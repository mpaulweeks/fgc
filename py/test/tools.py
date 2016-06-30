
import unittest
from py.test.datagen import (
    ensure_test_data,
    sample_player_id,
    sample_matches,
)


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ensure_test_data()
        cls.sample_player_id = sample_player_id
        cls.setUpChildClass()

    @classmethod
    def setUpChildClass(cls):
        # to be overridden
        pass

    @classmethod
    def sample_matches(cls):
        return sample_matches()
