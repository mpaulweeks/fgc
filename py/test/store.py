
from py.test.tools import (
    BaseTestCase,
)
from py.test.datagen import (
    create_test_player,
)
from py.src.store import (
    get_subscribed_player_count,
)


class StoreTest(BaseTestCase):

    def test_count_subscribed(self):
        create_test_player(subscribed=True)
        create_test_player(subscribed=True)
        create_test_player(subscribed=True)
        create_test_player(subscribed=False)
        self.assertEqual(4, get_subscribed_player_count())
