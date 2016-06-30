
from collections import defaultdict
from py.src.logger import log
from py.src.match.model.cfn import (
    CFNMatchModel,
    CFNRoundModel,
)


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class OpponentData():

    def __init__(self, opponent_character_id=None, opp_dict=None):
        self.character_id = (
            opp_dict['id'] if opp_dict else opponent_character_id
        )
        self.game_count = opp_dict['gc'] if opp_dict else 0
        self.game_wins = opp_dict['gw'] if opp_dict else 0
        self.round_count = opp_dict['rc'] if opp_dict else 0
        self.round_wins = opp_dict['rw'] if opp_dict else 0
        round_type_dict = opp_dict['rt'] if opp_dict else None
        round_type_lookup = {}
        if round_type_dict:
            for round_type_key, round_type_count in round_type_dict.items():
                int_key = int(round_type_key)
                round_type_lookup[int_key] = round_type_count
        self.round_types = defaultdict(
            int,
            round_type_lookup,
        )

    def to_dict(self):
        return {
            'id': self.character_id,
            'gc': self.game_count,
            'gw': self.game_wins,
            'rc': self.round_count,
            'rw': self.round_wins,
            'rt': dict(self.round_types),
        }

    @classmethod
    def from_character_id(caller, opponent_character_id):
        return OpponentData(opponent_character_id=opponent_character_id)

    def combine(self, other_opponent_data):
        if self.character_id != other_opponent_data.character_id:
            raise Exception
        new_opponent_data = OpponentData(
            opp_dict=other_opponent_data.to_dict()
        )
        new_opponent_data.game_count += self.game_count
        new_opponent_data.game_wins += self.game_wins
        new_opponent_data.round_count += self.round_count
        new_opponent_data.round_wins += self.round_wins
        for round_type, type_count in self.round_types.items():
            new_opponent_data.round_types[round_type] += type_count
        return new_opponent_data


class CharacterData():

    def __init__(self, character_id=None, char_dict=None):
        self.character_id = char_dict['id'] if char_dict else character_id
        opp_lookup = {}
        if char_dict:
            for opp_dict in char_dict['o'].values():
                opp_data = OpponentData(opp_dict=opp_dict)
                opp_lookup[opp_data.character_id] = opp_data
        self.opponents = keydefaultdict(
            OpponentData.from_character_id,
            opp_lookup,
        )

    def to_dict(self):
        opp_lookup = {}
        for opp_key, opp_data in self.opponents.items():
            opp_lookup[opp_key] = opp_data.to_dict()
        return {
            'id': self.character_id,
            'o': opp_lookup,
        }

    @classmethod
    def from_character_id(caller, character_id):
        return CharacterData(character_id=character_id)

    def calculate_stats(self):
        self.game_count = 0
        self.game_wins = 0
        self.round_count = 0
        self.round_wins = 0
        self.round_types = defaultdict(int)
        for opp_data in self.opponents.values():
            self.game_count += opp_data.game_count
            self.game_wins += opp_data.game_wins
            self.round_count += opp_data.round_count
            self.round_wins += opp_data.round_wins
            for round_type, type_count in opp_data.round_types.items():
                self.round_types[round_type] += type_count

    def combine(self, other_character_data):
        if self.character_id != other_character_data.character_id:
            raise Exception
        new_character_data = CharacterData(
            char_dict=other_character_data.to_dict()
        )
        for opp_key, opp_data in self.opponents.items():
            new_character_data.opponents[opp_key] = (
                new_character_data.opponents[opp_key].combine(opp_data)
            )
        return new_character_data


class _BasePlayerData():

    def __init__(self, player_dict=None):
        char_lookup = {}
        if player_dict:
            for char_dict in player_dict['c'].values():
                char_data = CharacterData(char_dict=char_dict)
                char_lookup[char_data.character_id] = char_data
        self.characters = keydefaultdict(
            CharacterData.from_character_id,
            char_lookup,
        )

    def to_dict(self):
        char_lookup = {}
        for char_key, char_data in self.characters.items():
            char_lookup[char_key] = char_data.to_dict()
        return {
            'c': char_lookup,
        }

    def calculate_stats(self):
        self.game_count = 0
        self.game_wins = 0
        self.round_count = 0
        self.round_wins = 0
        self.round_types = defaultdict(int)
        for char_data in self.characters.values():
            char_data.calculate_stats()
            self.game_count += char_data.game_count
            self.game_wins += char_data.game_wins
            self.round_count += char_data.round_count
            self.round_wins += char_data.round_wins
            for round_type, type_count in char_data.round_types.items():
                self.round_types[round_type] += type_count
        self.most_used_character = max(
            self.characters.keys(),
            key=lambda cid: self.characters[cid].game_count,
        ) if self.characters else None

    def combine(self, other_player_data):
        new_player = _BasePlayerData(other_player_data.to_dict())
        for char_key, char_data in self.characters.items():
            new_player.characters[char_key] = (
                new_player.characters[char_key].combine(char_data)
            )
        return new_player

    def _process_matches(
            self,
            matches,
            is_current_player_func,
            is_new_match_func
            ):
        latest_new_match = None
        latest_any_match = None
        for match_dict in matches:
            match = CFNMatchModel(match_dict, is_current_player_func)
            if not latest_any_match or match.ticks > latest_any_match.ticks:
                latest_any_match = match
            if not is_new_match_func(match):
                continue
            if not latest_new_match or match.ticks > latest_new_match.ticks:
                latest_new_match = match
            player = match.player
            opponent = match.opponent
            matchup = (
                self
                .characters[player.char_id]
                .opponents[opponent.char_id]
            )
            matchup.game_count += 1
            if match.winner_id == player.cfn_id:
                matchup.game_wins += 1
            for mr_dict in match.rounds:
                matchup.round_count += 1
                mr = CFNRoundModel(mr_dict)
                if mr.winner_id == player.cfn_id:
                    matchup.round_wins += 1
                    matchup.round_types[mr.round_type] += 1
        self.latest_new_match = latest_new_match
        self.latest_any_match = latest_any_match


class IndividualPlayerData(_BasePlayerData):

    def __init__(self, player_id=None, player_dict=None):
        if player_id and player_dict and player_id != player_dict['id']:
            raise Exception
        self.player_id = player_dict['id'] if player_dict else player_id
        self.is_updated = False
        self.latest_match_ticks = player_dict['lm'] if player_dict else None
        self.league_points = player_dict['lp'] if player_dict else None
        super(IndividualPlayerData, self).__init__(player_dict=player_dict)

    def to_dict(self):
        res_dict = super(IndividualPlayerData, self).to_dict()
        res_dict.update({
            'id': self.player_id,
            'lm': self.latest_match_ticks,
            'lp': self.league_points,
        })
        return res_dict

    def _is_current_player(self, cfn_player):
        return cfn_player.cfn_id == self.player_id

    def _is_new_match(self, match):
        return (
            self.latest_match_ticks is None or
            match.ticks > self.latest_match_ticks
        )

    def _process_matches(self, matches):
        super(IndividualPlayerData, self)._process_matches(
            matches,
            self._is_current_player,
            self._is_new_match,
        )
        if self.latest_new_match:
            self.latest_match_ticks = self.latest_new_match.ticks
            if self.latest_new_match.player.league_points > 0:
                # sometimes get bad LP data from Capcom, check before updating
                self.league_points = self.latest_new_match.player.league_points
        if self.latest_any_match:
            self.region = self.latest_any_match.player.region
            self.platform = self.latest_any_match.player.platform


class RankBinPlayerData(_BasePlayerData):

    def __init__(
            self,
            player_bin=None,
            opponent_bin=None,
            player_dict=None,
            ):
        if player_bin and player_dict and player_bin != player_dict['pb']:
            raise Exception
        if opponent_bin and player_dict and opponent_bin != player_dict['ob']:
            raise Exception
        self.player_bin = player_dict['pb'] if player_dict else player_bin
        self.opponent_bin = player_dict['ob'] if player_dict else opponent_bin
        super(RankBinPlayerData, self).__init__(player_dict=player_dict)

    def to_dict(self):
        res_dict = super(RankBinPlayerData, self).to_dict()
        res_dict.update({
            'pb': self.player_bin,
            'ob': self.opponent_bin,
        })
        return res_dict

    def _process_matches(
            self,
            matches,
            is_current_player_func,
            ):
        super(RankBinPlayerData, self)._process_matches(
            matches,
            is_current_player_func,
            lambda cfn_match: True,
        )


class _BaseRankBinMatchupData():

    def get_player_data_for_bin(self, rank_bin):
        for player_data in self.all_player_data:
            if player_data.player_bin == rank_bin:
                return player_data
        raise Exception


class RankBinMatchupPair(_BaseRankBinMatchupData):

    def __init__(
            self,
            lower_bin=None,
            higher_bin=None,
            matchup_dict=None,
            ):
        self.lower_bin = matchup_dict['lb'] if matchup_dict else lower_bin
        self.higher_bin = matchup_dict['hb'] if matchup_dict else higher_bin
        lower_player_dict = matchup_dict['ld'] if matchup_dict else None
        higher_player_dict = matchup_dict['hd'] if matchup_dict else None
        self.lower_player_data = RankBinPlayerData(
            self.lower_bin, self.higher_bin, lower_player_dict
        )
        self.higher_player_data = RankBinPlayerData(
            self.higher_bin, self.lower_bin, higher_player_dict
        )
        self.all_player_data = [
            self.lower_player_data,
            self.higher_player_data,
        ]

    def to_dict(self):
        return {
            'lb': self.lower_bin,
            'ld': self.lower_player_data.to_dict(),
            'hb': self.higher_bin,
            'hd': self.higher_player_data.to_dict(),
        }

    def _process_matches(self, matches):
        self.lower_player_data._process_matches(
            matches,
            lambda cfn_player: cfn_player.rank_bin == self.lower_bin,
        )
        self.higher_player_data._process_matches(
            matches,
            lambda cfn_player: cfn_player.rank_bin == self.higher_bin,
        )


class RankBinMatchupMirror(_BaseRankBinMatchupData):

    def __init__(
            self,
            mirror_bin=None,
            matchup_dict=None,
            ):
        self.mirror_bin = matchup_dict['mb'] if matchup_dict else mirror_bin
        mirror_player_dict = matchup_dict['md'] if matchup_dict else None
        self.mirror_player_data = RankBinPlayerData(
            self.mirror_bin, self.mirror_bin, mirror_player_dict
        )
        self.all_player_data = [
            self.mirror_player_data,
        ]

    @property
    def lower_bin(self):
        return self.mirror_bin

    @property
    def higher_bin(self):
        return self.mirror_bin

    def to_dict(self):
        return {
            'mb': self.mirror_bin,
            'md': self.mirror_player_data.to_dict(),
        }

    def _process_matches(self, matches):
        self.mirror_player_data._process_matches(
            matches,
            lambda cfn_player: True,
        )
        self.mirror_player_data._process_matches(
            matches,
            lambda cfn_player: False,
        )


def _rbm_decider(rbm_dict):
    if 'mb' in rbm_dict:
        return RankBinMatchupMirror(matchup_dict=rbm_dict)
    elif 'lb' in rbm_dict:
        return RankBinMatchupPair(matchup_dict=rbm_dict)
    else:
        raise Exception


def _rbm_creator_factory(lower_bin):
    def rbm_creator(higher_bin):
        if lower_bin == higher_bin:
            return RankBinMatchupMirror(
                mirror_bin=lower_bin
            )
        elif lower_bin < higher_bin:
            return RankBinMatchupPair(
                lower_bin=lower_bin,
                higher_bin=higher_bin,
            )
        else:
            raise Exception
    return rbm_creator


class LowerRankBinData():

    def __init__(
            self,
            lower_bin=None,
            bin_dict=None
            ):
        self.lower_bin = bin_dict['lb'] if bin_dict else lower_bin
        rbm_lookup = {}
        if bin_dict:
            for rbm_dict in bin_dict['rbm'].values():
                rbm_data = _rbm_decider(rbm_dict)
                if self.lower_bin != rbm_data.lower_bin:
                    raise Exception
                rbm_lookup[rbm_data.higher_bin] = rbm_data
        self.rank_bin_matchups = keydefaultdict(
            _rbm_creator_factory(self.lower_bin),
            rbm_lookup,
        )

    def to_dict(self):
        rbm_lookup = {}
        for rbm_key, rbm_data in self.rank_bin_matchups.items():
            rbm_lookup[rbm_key] = rbm_data.to_dict()
        return {
            'lb': self.lower_bin,
            'rbm': rbm_lookup,
        }

    @classmethod
    def from_lower_bin(caller, lower_bin):
        return LowerRankBinData(lower_bin=lower_bin)

    def _process_matches(
            self,
            matches_by_higher_bin,
            ):
        for higher_bin_key, matches in matches_by_higher_bin.items():
            self.rank_bin_matchups[higher_bin_key]._process_matches(
                matches,
            )


class GlobalRankedData():

    def __init__(
            self,
            global_dict=None,
            ):
        bin_lookup = {}
        if global_dict:
            for bin_dict in global_dict['b'].values():
                bin_data = LowerRankBinData(bin_dict=bin_dict)
                bin_lookup[bin_data.lower_bin] = bin_data
        self.lower_rank_bins = keydefaultdict(
            LowerRankBinData.from_lower_bin,
            bin_lookup,
        )

    def to_dict(self):
        bin_lookup = {}
        for bin_key, bin_data in self.lower_rank_bins.items():
            bin_lookup[bin_key] = bin_data.to_dict()
        return {
            'b': bin_lookup,
        }

    def _process_matches(
            self,
            matches,
            is_new_match_func,
            ):
        match_bins = defaultdict(lambda: defaultdict(list))
        for match_dict in matches:
            match = CFNMatchModel(match_dict)
            if not is_new_match_func(match):
                continue
            lower_bin = match_bins[match.lower_rank.rank_bin]
            lower_bin[match.higher_rank.rank_bin].append(match_dict)
        for lower_bin_key, higher_bin_matches in match_bins.items():
            self.lower_rank_bins[lower_bin_key]._process_matches(
                higher_bin_matches
            )

    def _combine_player_data(self, player_datas):
        new_player = _BasePlayerData()
        for player_data in player_datas:
            new_player = new_player.combine(player_data)
        return new_player

    def get_player_data_by_bins(
            self,
            p1_bins,
            p2_bins,
            ):
        player_datas = []
        for p1_bin in p1_bins:
            for p2_bin in p2_bins:
                lower_bin = min(p1_bin, p2_bin)
                higher_bin = max(p1_bin, p2_bin)
                player_data = (
                    self
                    .lower_rank_bins[lower_bin]
                    .rank_bin_matchups[higher_bin]
                    .get_player_data_for_bin(p1_bin)
                )
                player_datas.append(player_data)
        combined = self._combine_player_data(player_datas)
        return combined
