
import json
from py.src.logger import log
from py.src.store import (
    load_player_ids_to_backfill,
)
from py.src.match.model.cache import (
    MatchCache,
)
from py.src.settings import (
    DATABASE,
)
from py.src.db.model import (
    Match,
    Player,
)


def load_player_match_history(pid):
    return list(
        Match
        .select()
        .where(
            (Match.left_player_cfn_id == pid) |
            (Match.right_player_cfn_id == pid)
        )
    )


def backload_player(cache, player_id):
    match_history = load_player_match_history(player_id)
    matches = [json.loads(m.data) for m in match_history]

    player = cache.process_matches(player_id, matches)
    return player


def backload_all_players():
    log('backloading match_last_updated players')
    log('building cache')
    cache = MatchCache()
    batch_size = 500
    backfill_player_ids = load_player_ids_to_backfill(
        batch_size=batch_size,
    )
    log('backloading %s players...' % batch_size)
    for player_id in backfill_player_ids:
        backload_player(cache, player_id)
    log("saving")
    cache.save()
    log("done")


def load_volatile_player_ids(
        subset_ids=None,
        batch_size=None,
        ):
    query = (
        Player
        .select()
        .where(Player.subscribed == 1)
    )
    if subset_ids:
        query = (
            query
            .where(Player.cfn_id << list(subset_ids))
        )
    if batch_size:
        query = (
            query
            .order_by(Player.updated_at.desc())
            .limit(batch_size)
        )
    return set([
        p.cfn_id for p in query
    ])


def backload_volatile_players():
    log('backloading volatile players')
    log('building cache')
    cache = MatchCache()
    batch_size = 600
    backfill_player_ids = load_volatile_player_ids(
        batch_size=batch_size,
    )
    log('backloading %s players...' % batch_size)
    for player_id in backfill_player_ids:
        backload_player(cache, player_id)
    log("saving")
    cache.save()
    log("done")


if __name__ == "__main__":
    DATABASE.connect()
    backload_all_players()
    if not DATABASE.is_closed():
        DATABASE.close()
