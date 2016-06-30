
from unittest import mock

from py.test.tools import (
    BaseTestCase,
)
from py.src.match.model.data import (
    GlobalRankedData,
)
from py.src.view_model import (
    GlobalViewModelCache,
)


class GlobalIntegrationTest(BaseTestCase):

    @classmethod
    def setUpChildClass(cls):
        cls.matches = cls.sample_matches()

    def _create_global_view_model(self, global_dict):
        with mock.patch(
            'py.src.view_model.get_global_ranked_match_cache',
        ) as mp:
            mp.return_value = global_dict
            return GlobalViewModelCache()

    def test_global(self):
        global_data = GlobalRankedData(global_dict=None)
        global_data._process_matches(self.matches, lambda m: True)
        vm_cache = self._create_global_view_model(global_data.to_dict())
        global_vm = vm_cache.get_by_leagues([], [])
        self.assertEqual(188, global_vm.data.game_count)
        self.assertEqual(94, global_vm.data.game_wins)
        self.assertEqual(47, global_vm.data.characters[14].game_count)

    def test_to_dict(self):
        global_data = GlobalRankedData(global_dict=None)
        global_data._process_matches(self.matches, lambda m: True)
        dict1 = global_data.to_dict()
        dict2 = GlobalRankedData(global_dict=dict1).to_dict()
        self.assertEqual(dict1, dict2)
