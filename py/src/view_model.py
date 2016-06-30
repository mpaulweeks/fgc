
from py.src.store import (
    get_latest_player_updated_at,
)
from py.src.repo import (
    get_player_rankings,
    get_player_by_name,
    get_global_ranked_match_cache,
)
from py.src.time_util import (
    convert_dt_to_nyc,
    convert_ticks_to_nyc,
)
from py.src.cfn import cfn_constants
from py.src.match.model.cfn import (
    CFNLeagueCache,
)
from py.src.match.model.data import (
    IndividualPlayerData,
    GlobalRankedData,
)


class LeaderboardViewModel():

    def __init__(self):
        self.player_rankings = sorted(
            get_player_rankings(),
            key=lambda pr: pr.placement,
        )
        self.updated_time = convert_dt_to_nyc(
            self.player_rankings[0].created_at
        )
        for pr in self.player_rankings:
            pr.league = CFNLeagueCache.from_league_points(pr.league_points)
            pr.favorite_character = CharacterViewModel(
                pr.favorite_character_id
            )
            pr.most_used_character = CharacterViewModel(
                pr.most_used_character_id
            )


class CharacterViewModel():

    def __init__(self, character_id):
        self.character_id = character_id

    @property
    def name(self):
        return cfn_constants.CHARACTERS.get(self.character_id, 'N/A')

    @property
    def img(self):
        return cfn_constants.CHARACTER_IMG.get(self.character_id, '')


def sort_characters(player_data):
    unsorted_characters = []
    for char in player_data.characters.values():
        if char.game_count == 0:
            continue
        unsorted_opponents = []
        for opp in char.opponents.values():
            if opp.game_count == 0:
                continue
            unsorted_opponents.append(opp)
        sorted_opponents = sorted(
            unsorted_opponents,
            reverse=True,
            key=lambda d: d.game_count,
        )
        char.opponents_sorted = sorted_opponents
        unsorted_characters.append(char)
    sorted_characters = sorted(
        unsorted_characters,
        reverse=True,
        key=lambda d: d.game_count,
    )
    player_data.characters_sorted = sorted_characters


class _BaseViewModel():
    is_global = False
    is_filter = False

    def __init__(self, player_data):
        # template expects these declared, up to subclasses to define
        self.name = "???"
        self.latest_match_date = None
        self.updated_date = None

        self.cfn_league_cache = CFNLeagueCache

        self.data = player_data
        self.data.calculate_stats()
        for char_data in self.data.characters.values():
            char_data.vm = CharacterViewModel(char_data.character_id)
            for opp_data in char_data.opponents.values():
                opp_data.vm = CharacterViewModel(opp_data.character_id)
        sort_characters(self.data)
        self.total_match_count = self.data.game_count
        self.data_exists = self.total_match_count > 0


class PlayerViewModel(_BaseViewModel):

    def __init__(self, player, player_data):
        self.player = player
        super(PlayerViewModel, self).__init__(player_data)

        self.name = self.player.name
        self.latest_match_date = convert_ticks_to_nyc(
            self.player.match_latest_ticks
        )
        self.updated_date = convert_dt_to_nyc(
            self.player.match_updated_at
        )
        self.league_points = self.data.league_points
        self.league = self.cfn_league_cache.from_league_points(
            self.league_points
        )


class WinTypeViewModel():

    def __init__(
            self,
            name,
            best,
            worst,
            ):
        self.name = name
        self.best = best
        self.worst = worst


class GlobalViewModel(_BaseViewModel):
    is_global = True

    def __init__(
            self,
            global_data,
            p1_league_codes,
            p2_league_codes,
            ):
        self.p1_league_codes = set(p1_league_codes)
        self.p2_league_codes = set(p2_league_codes)
        player_data = global_data.get_player_data_by_bins(
            CFNLeagueCache.convert_leagues_to_bins(self.p1_league_codes),
            CFNLeagueCache.convert_leagues_to_bins(self.p2_league_codes),
        )
        super(GlobalViewModel, self).__init__(player_data)
        self._analyze_round_data()

        self.name = "CHARACTER MATCHUPS BY LEAGUE"
        self.updated_date = convert_dt_to_nyc(
            get_latest_player_updated_at()
        )
        self.total_match_count = self.data.game_count // 2

        self.character_order = list(map(
            CharacterViewModel, cfn_constants.CHARACTER_ORDER
        ))
        all_league_codes = CFNLeagueCache.all_league_codes()
        self.p1_all_leagues = self.p1_league_codes == all_league_codes
        self.p2_all_leagues = self.p2_league_codes == all_league_codes

    def calc_win_ratio_factory(self, win_type):
        def calc_win_ratio(character_data):
            if character_data.round_wins == 0:
                return 0
            return (
                character_data.round_types[win_type] /
                character_data.round_wins
            )
        return calc_win_ratio

    def _analyze_round_data(self):
        if not self.data_exists:
            return
        self.win_types = {}
        character_datas = self.data.characters.values()
        for win_type, name in cfn_constants.WIN_TYPES.items():
            win_ratio_func = self.calc_win_ratio_factory(win_type)
            self.win_types[win_type] = WinTypeViewModel(
                name=name,
                best=max(character_datas, key=win_ratio_func).vm,
                worst=min(character_datas, key=win_ratio_func).vm,
            )

    def bins_match(self, p1_league_codes, p2_league_codes):
        return (
            self.p1_league_codes == set(p1_league_codes) and
            self.p2_league_codes == set(p2_league_codes)
        )


class PlayerViewModelCache():

    def __init__(self):
        self.pvm_by_name = {}

    def get_by_name(self, player_name):
        if player_name not in self.pvm_by_name:
            player = get_player_by_name(player_name)
            player_data = IndividualPlayerData(
                player.cfn_id,
                player.get_match_cache(),
            )
            self.pvm_by_name[player.name] = PlayerViewModel(
                player=player,
                player_data=player_data,
            )
        return self.pvm_by_name[player_name]


class GlobalViewModelCache():

    def __init__(self):
        self.global_data = GlobalRankedData(
            global_dict=get_global_ranked_match_cache(),
        )
        self.cached_vms = []
        self.get_by_leagues(
            p1_league_codes=[],
            p2_league_codes=[],
        )

    def get_by_leagues(self, p1_league_codes, p2_league_codes):
        p1_league_codes = p1_league_codes or CFNLeagueCache.all_league_codes()
        p2_league_codes = p2_league_codes or CFNLeagueCache.all_league_codes()
        for gvm in self.cached_vms:
            if gvm.bins_match(p1_league_codes, p2_league_codes):
                return gvm
        # else if no match
        new_global_view_model = GlobalViewModel(
            self.global_data,
            p1_league_codes,
            p2_league_codes,
        )
        self.cached_vms.append(new_global_view_model)
        return new_global_view_model
