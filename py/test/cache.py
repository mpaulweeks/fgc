
from unittest import mock

from py.test.tools import (
    BaseTestCase,
)
from py.src.db.model import (
    Player,
)
from py.src.match.model.cache import (
    MatchCache,
)
from py.src.match.model.cfn import (
    CFNLeagueCache,
)


class CFNLeagueCacheTest(BaseTestCase):

    def test_leagues_declared(self):
        self.assertEqual(14, len(CFNLeagueCache.leagues()))

    def test_leagues_unique(self):
        bounds = set()
        for league in CFNLeagueCache.leagues():
            self.assertNotIn(league.lower_bound, bounds)
            bounds.add(league.lower_bound)
            self.assertNotIn(league.upper_bound, bounds)
            bounds.add(league.upper_bound)
        bins = set()
        for league in CFNLeagueCache.leagues():
            for league_bin in league.bins:
                self.assertNotIn(league_bin, bins)
                bins.add(league_bin)


class MatchCacheTest(BaseTestCase):

    @classmethod
    def setUpChildClass(cls):
        cls.player_id = cls.sample_player_id
        cls.bad_player_id = -1
        cls.matches = cls.sample_matches()

    def setUp(self):
        self.cache = self._create_cache()

    def _create_cache(self):
        with mock.patch(
            'py.src.match.model.cache.download_global_cache'
        ) as m_dw:
            with mock.patch(
                'py.src.match.model.cache.get_player_ticks'
            ) as m_pt:
                with mock.patch(
                    'py.src.match.model.cache.get_global_ranked_match_cache'
                ) as m_gc:
                    m_pt.return_value = {}
                    m_gc.return_value = None
                    cache = MatchCache()
                    self.assertEqual(1, m_dw.call_count)
                    return cache

    def process_matches(self, player_id, matches):
        with mock.patch(
            'py.src.match.model.cache.load_player_by_id'
        ) as m_lp:
            mock_player = Player()
            mock_player.cfn_id = player_id
            m_lp.return_value = mock_player
            return self.cache.process_matches(player_id, matches)

    def test_process_matches_updates_cache(self):
        self.process_matches(self.player_id, [self.matches[0]])
        self.assertEqual(
            635912839286230032,
            self.cache.player_ticks[self.player_id],
        )
        before_global = self.cache.global_data.to_dict()
        self.process_matches(self.player_id, self.matches)
        self.assertEqual(
            635928986469343632,
            self.cache.player_ticks[self.player_id],
        )
        after_global = self.cache.global_data.to_dict()
        self.assertNotEqual(before_global, after_global)

    def test_process_matches_idempotent(self):
        self.process_matches(self.player_id, self.matches)
        before_ticks = self.cache.player_ticks.copy()
        before_global = self.cache.global_data.to_dict()
        self.process_matches(self.player_id, self.matches)
        after_ticks = self.cache.player_ticks.copy()
        after_global = self.cache.global_data.to_dict()
        self.assertEqual(before_ticks, after_ticks)
        self.assertEqual(before_global, after_global)

    def test_process_matches_no_matches_ok(self):
        player = self.process_matches(self.player_id, [])
        self.assertEqual(self.player_id, player.cfn_id)
        self.assertEqual(None, player.get_match_cache())

    @mock.patch('py.src.match.model.cache.save_player_cache')
    @mock.patch('py.src.match.model.cache.save_global_ranked_match_cache')
    def test_save_cache(self, global_mock, player_mock):
        self.process_matches(self.player_id, self.matches)
        self.process_matches(self.bad_player_id, [])
        self.assertEqual(0, player_mock.call_count)
        self.assertEqual(0, global_mock.call_count)
        self.cache.save()
        self.assertEqual(2, player_mock.call_count)
        self.assertEqual(1, global_mock.call_count)
