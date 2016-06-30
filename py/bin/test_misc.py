#!/usr/bin/env python3

from py.src.logger import log
from py.src.message import (
    send_error_message,
)
from py.src.settings import (
    DATABASE,
)
from py.src.cfn.api import (
    create_session,
    test_cookie_status,
    query_cfn,
    fix_player_names,
    batch_query_match_history,
    MATCH_URL,
    RIVAL_URL,
)

import logging
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def test_rival(rival_name):
    url = RIVAL_URL % ("%s", rival_name)
    with create_session() as session:
        res = query_cfn(session, url)
        log(res)
        log(res.headers)
        log(res.text)


def pull_one_player_data():
    with create_session() as session:
        test_cookie_status(session)
        DATABASE.connect()
        pids = [2728664320]
        batch_query_match_history(session, pids)
        fix_player_names(session)
    if not DATABASE.is_closed():
        DATABASE.close()


def query_match_data(player_id=None):
    player_id = player_id or 5153458176
    url = MATCH_URL % ('%s', player_id)
    with create_session() as session:
        res = query_cfn(session, url)
    log(res.text)
    return res.json()['response'][0]


def main():
    log('use this by importing module')


if __name__ == "__main__":
    main()
