
from datetime import datetime
import json
from py.src.logger import log
from py.src.db.api import (
    ensure_test_tables,
)
from py.src.db.model import (
    Match,
    Player,
    Rank,
)

sample_player_id = 2728664320


def sample_matches():
    with open('py/test/match_data.json') as matches_file:
        return json.load(matches_file)


_test_data_created = False
_id_counter = 1


def ensure_test_data():
    global _test_data_created
    if _test_data_created:
        return
    _test_data_created = True
    ensure_test_tables()
    log('creating test data')
    already_exists = (
        Player
        .select()
        .where(Player.cfn_id == sample_player_id)
        .exists()
    )
    if already_exists:
        log('existing test data found')
        return
    create_test_player(
        cfn_id=sample_player_id,
        name='TestPlayer',
        subscribed=True,
    )
    Rank.create(
        id=1,
        created_at=datetime.utcnow(),
        player_cfn=sample_player_id,
        league_points=100,
        placement=1,
        favorite_character=1,
    )


def create_test_player(cfn_id=None, name=None, subscribed=False):
    global _id_counter
    _id_counter += 1
    cfn_id = cfn_id or _id_counter
    name = name or 'Player #%s' % _id_counter
    subscribed = 1 if subscribed else 0
    return Player.create(
        cfn_id=cfn_id,
        name=name,
        subscribed=subscribed,
    )
