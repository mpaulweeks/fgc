#!/usr/bin/env python3

from py.src.logger import (
    log,
    log_exception,
    set_log_file,
)
from py.src.settings import (
    DATABASE,
)
from py.src.message import (
    send_error_message,
)
from py.src.cfn.api import (
    create_session,
    test_cookie_status,
    batch_query_match_history,
    fix_player_names,
)
from py.src.store import (
    load_subscribed_player_ids,
)

PLAYER_BATCH_SIZE = 300

if __name__ == "__main__":
    set_log_file("task_matches")
    log("task_matches begin")
    with create_session() as session:
        try:
            test_cookie_status(session)
            DATABASE.connect()
            pids = load_subscribed_player_ids(batch_size=PLAYER_BATCH_SIZE)
            any_error = batch_query_match_history(session, pids)
            fix_player_names(session)
        except Exception as e:
            log_exception(e)
            send_error_message("FATAL ERROR when pulling match data")
        else:
            if any_error:
                # suppress non-fatal errors for now
                # send_error_message('non-fatal errors when pulling matches')
                pass
    if not DATABASE.is_closed():
        DATABASE.close()
    log("task_matches complete")
