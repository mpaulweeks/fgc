#!/usr/bin/env python3

from py.src.logger import log
from py.src.settings import (
    DATABASE,
)
from py.src.cfn.api import (
    create_session,
    test_cookie_status,
    batch_query_match_history,
    fix_player_names,
)
from py.src.store import (
    load_player_rankings,
    load_subscribed_player_ids,
)

PLAYER_BATCH_SIZE = 50

if __name__ == "__main__":
    with create_session() as session:
        test_cookie_status(session)
        DATABASE.connect()
        latest_ranking = load_player_rankings()
        ranked_pids = [
            pr.player_cfn_id for pr in latest_ranking
        ]
        pids = load_subscribed_player_ids(
            subset_ids=ranked_pids,
            batch_size=PLAYER_BATCH_SIZE,
        )
        batch_query_match_history(session, pids)
        fix_player_names(session)
    if not DATABASE.is_closed():
        DATABASE.close()
