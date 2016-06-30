
from py.src.logger import log

LEAGUE_BIN_SIZE = 500  # dont ever change this


class CFNPlayerSearchModel():

    def __init__(self, player_dict):
        self.name = player_dict['fightersid']
        self.cfn_id = int(player_dict['publicid'])
        self.region = player_dict['region']
        self.platform = player_dict['accountsource']


class CFNPlayerMatchModel():

    def __init__(self, player_dict):
        self.cfn_id = int(player_dict['publicid'])
        self.region = player_dict['region']
        self.platform = player_dict['accountsource']
        self.char_id = int(player_dict['characterid'])
        self.league_points = int(player_dict['leaguepoint'])
        self.rank_bin = self.league_points // LEAGUE_BIN_SIZE


class CFNRoundModel():

    def __init__(self, round_dict):
        self.winner_id = int(round_dict['winner'])
        self.round_type = int(round_dict['wintype'])


class CFNMatchModel():

    def __init__(self, match_dict, is_current_player=None):
        self.ticks = int(match_dict['matchtime'])
        self.winner_id = int(match_dict['winner'])
        self.rounds = match_dict['rounds']
        self.left_player = CFNPlayerMatchModel(
            match_dict['leftstartplayerinfo'][0]
        )
        self.right_player = CFNPlayerMatchModel(
            match_dict['rightstartplayerinfo'][0]
        )
        if self.left_player.league_points <= self.right_player.league_points:
            self.lower_rank = self.left_player
            self.higher_rank = self.right_player
        else:
            self.higher_rank = self.left_player
            self.lower_rank = self.right_player
        if is_current_player:
            if is_current_player(self.left_player):
                self.player = self.left_player
                self.opponent = self.right_player
            else:
                self.opponent = self.left_player
                self.player = self.right_player


class CFNLeagueModel():

    def __init__(self, name, lower_bound, upper_bound):
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        if self.lower_bound >= self.upper_bound:
            raise Exception

    @property
    def code(self):
        return self.name.replace(' ', '')

    @property
    def bins(self):
        bins = set()
        current_lp = self.lower_bound
        while current_lp < self.upper_bound:
            bins.add(current_lp // LEAGUE_BIN_SIZE)
            current_lp += LEAGUE_BIN_SIZE
        return bins


class CFNLeagueCache():
    # singleton
    _leagues = {}

    def __init__(self):
        raise Exception

    @classmethod
    def declare(cls, lower_bound, upper_bound, name):
        lm = CFNLeagueModel(
            name,
            lower_bound,
            upper_bound,
        )
        cls._leagues[lm.code] = lm

    @classmethod
    def leagues(self):
        return sorted(
            self._leagues.values(),
            reverse=True,
            key=lambda lm: lm.lower_bound,
        )

    @classmethod
    def all_league_codes(cls):
        return set([lm.code for lm in cls._leagues.values()])

    @classmethod
    def convert_leagues_to_bins(cls, league_codes):
        bins = set()
        for code in league_codes:
            bins.update(cls._leagues[code].bins)
        return bins

    @classmethod
    def from_league_points(cls, league_points):
        if league_points is None:
            return None
        sorted_leagues = cls.leagues()
        for league in sorted_leagues:
            if league_points >= league.lower_bound:
                return league
        raise Exception('league_points < 0 not valid')


CFNLeagueCache.declare(14000, 19999, 'Diamond')  # unknown whats next
CFNLeagueCache.declare(12000, 13999, 'Ultra Platinum')
CFNLeagueCache.declare(10000, 11999, 'Super Platinum')
CFNLeagueCache.declare(7500, 9999, 'Platinum')
CFNLeagueCache.declare(6500, 7499, 'Ultra Gold')
CFNLeagueCache.declare(5500, 6499, 'Super Gold')
CFNLeagueCache.declare(4000, 5499, 'Gold')
CFNLeagueCache.declare(3500, 3999, 'Ultra Silver')
CFNLeagueCache.declare(3000, 3499, 'Super Silver')
CFNLeagueCache.declare(2000, 2999, 'Silver')
CFNLeagueCache.declare(1500, 1999, 'Ultra Bronze')
CFNLeagueCache.declare(1000, 1499, 'Super Bronze')
CFNLeagueCache.declare(500, 999, 'Bronze')
CFNLeagueCache.declare(0, 499, 'Rookie')
