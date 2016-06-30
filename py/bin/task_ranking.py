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
    record_top_players,
)


if __name__ == "__main__":
    set_log_file("task_ranking")
    log("task_ranking begin")
    with create_session() as session:
        try:
            test_cookie_status(session)
            DATABASE.connect()
            record_top_players(session)
        except Exception as e:
            log_exception(e)
            send_error_message("FATAL ERROR when pulling rank data")
    if not DATABASE.is_closed():
        DATABASE.close()
    log("task_ranking complete")
