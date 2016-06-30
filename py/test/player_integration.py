
from unittest import mock

from py.test.tools import (
    BaseTestCase,
)
from py.src.db.model import (
    Player,
)
from py.src.match.model.data import (
    IndividualPlayerData,
)
from py.src.match.model.cache import (
    update_player_with_matches,
)
from py.src.view_model import (
    PlayerViewModelCache,
)


class PlayerCacheTest(BaseTestCase):

    @classmethod
    def setUpChildClass(cls):
        cls.player_id = cls.sample_player_id
        cls.matches = cls.sample_matches()

    def test_individual_player(self):
        player = Player(cfn_id=self.player_id)
        update_player_with_matches(player, self.matches)
        vm_cache = PlayerViewModelCache()
        with mock.patch('py.src.view_model.get_player_by_name') as m:
            m.return_value = player
            player_vm = vm_cache.get_by_name(player.name)
        self.assertEqual(2728664320, player_vm.data.player_id)
        self.assertEqual(94, player_vm.data.game_count)
        self.assertEqual(62, player_vm.data.game_wins)
        self.assertEqual(2157, player_vm.league_points)
        self.assertEqual('USA', player_vm.player.region)
        self.assertEqual('steam', player_vm.player.platform)
        self.assertEqual(14, player_vm.data.most_used_character)
        self.assertEqual('2016-03-06', player_vm.latest_match_date)

    def test_individual_player_idempotent(self):
        player = Player(cfn_id=self.player_id)
        update_player_with_matches(player, self.matches)
        update_player_with_matches(player, self.matches)
        vm_cache = PlayerViewModelCache()
        with mock.patch('py.src.view_model.get_player_by_name') as m:
            m.return_value = player
            player_vm = vm_cache.get_by_name(player.name)
        self.assertEqual(2728664320, player_vm.data.player_id)
        self.assertEqual(94, player_vm.data.game_count)
        self.assertEqual(62, player_vm.data.game_wins)
        self.assertEqual(2157, player_vm.league_points)
        self.assertEqual('USA', player_vm.player.region)
        self.assertEqual('steam', player_vm.player.platform)
        self.assertEqual(14, player_vm.data.most_used_character)
        self.assertEqual('2016-03-06', player_vm.latest_match_date)

    def test_to_dict(self):
        player = Player(cfn_id=self.player_id)
        player_data = update_player_with_matches(player, self.matches)
        dict1 = player_data.to_dict()
        dict2 = IndividualPlayerData(player_dict=dict1).to_dict()
        self.assertEqual(dict1, dict2)

    def test_empty_ok(self):
        player = Player(cfn_id=self.player_id)
        vm_cache = PlayerViewModelCache()
        with mock.patch('py.src.view_model.get_player_by_name') as m:
            m.return_value = player
            player_vm = vm_cache.get_by_name(player.name)
        self.assertEqual(2728664320, player_vm.data.player_id)
        self.assertEqual(0, player_vm.data.game_count)
        self.assertEqual(0, player_vm.data.game_wins)
        self.assertEqual(None, player_vm.league_points)
        self.assertEqual(None, player_vm.player.region)
        self.assertEqual(None, player_vm.player.platform)
        self.assertEqual(None, player_vm.data.most_used_character)
        self.assertEqual(None, player_vm.latest_match_date)

    def test_player_combine(self):
        player = Player(cfn_id=self.player_id)
        player_data = update_player_with_matches(player, self.matches)
        dupe_pd = player_data
        dupe_pd = dupe_pd.combine(dupe_pd)
        dupe_pd = dupe_pd.combine(dupe_pd)
        dupe_pd.calculate_stats()
        self.assertEqual(376, dupe_pd.game_count)
