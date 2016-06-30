
from datetime import datetime
import json
from py.src.logger import log
from py.src.repo import (
    get_global_ranked_match_cache,
    get_player_ticks,
)
from py.src.store import (
    load_player_by_id,
    save_global_ranked_match_cache,
    save_player_cache,
)
from py.src.s3_store import (
    download_global_cache,
)
from py.src.match.model.data import (
    IndividualPlayerData,
    GlobalRankedData,
)


def update_player_with_matches(player, matches):
    player_data = IndividualPlayerData(
        player.cfn_id,
        player.get_match_cache(),
    )
    player_data._process_matches(matches)
    player.region = player_data.region
    player.platform = player_data.platform
    player.match_latest_ticks = player_data.latest_match_ticks
    player.match_data = json.dumps(
        player_data.to_dict(),
        sort_keys=True,
    )
    player_data.calculate_stats()
    player.match_character = player_data.most_used_character
    return player_data


class MatchCache():

    # ASSUMPTION: only one of these exists at a time
    # NEVER USE THIS IN A WEB REQUEST

    def __init__(self):
        download_global_cache()
        log("creating match cache")
        global_dict = get_global_ranked_match_cache()
        self._global_data = GlobalRankedData(global_dict=global_dict)
        self._player_ticks = get_player_ticks()
        self._players_to_save = []

    @property
    def player_ticks(self):
        return self._player_ticks

    @property
    def global_data(self):
        return self._global_data

    def is_new_global_match(self, cfn_match):
        player_ids = [
            cfn_match.left_player.cfn_id,
            cfn_match.right_player.cfn_id,
        ]
        for cfn_id in player_ids:
            current_ticks = self.player_ticks.get(cfn_id)
            if current_ticks and current_ticks >= cfn_match.ticks:
                return False
        return True

    def process_matches(self, player_id, matches):
        player = load_player_by_id(player_id)
        if matches:
            self.global_data._process_matches(
                matches,
                self.is_new_global_match,
            )
            update_player_with_matches(player, matches)
            self.player_ticks[player.cfn_id] = player.match_latest_ticks
        player.match_updated_at = datetime.utcnow()
        self._players_to_save.append(player)
        return player

    def save(self):
        log("saving match cache")
        for player in self._players_to_save:
            save_player_cache(player)
        # this implicitly uploads
        save_global_ranked_match_cache(self.global_data)
        self._players_to_save = []
        log("cache successfully saved")
