#!/usr/bin/env python3

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import json
from py.src.logger import (
    log,
    log_exception,
)
from py.src.settings import (
    DATABASE,
)
from py.src.error import (
    CookieInvalidException,
    MatchQueryException,
)
from py.src.message import (
    send_error_message,
)
from py.src.cfn.cookie import (
    wd_cookie,
    load_cookie_status,
    save_cookie_status,
)
from py.src.store import (
    save_match_list,
    save_ranking_results,
    set_player_updated_at,
    subscribe_to_new_player,
    Player,
)
from py.src.match.model.cache import (
    MatchCache,
)
from py.src.match.model.cfn import (
    CFNPlayerSearchModel,
)

# to save all the logging
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LICENSE_URL = '/bentov2/sf5/myinfo/%s/fighterlicense/%s'
RANKING_URL = '/bentov2/sf5/contents/%s/ranking;page=%s'
MATCH_URL = '/bentov2/sf5/myinfo/%s/match/%s;opponentfull:matchtype=0'  # this is just ranked
RIVAL_URL = '/bentov2/sf5/myinfo/%s/searchrival/fightersid;id=%s:sort=lp:page=1:sortdir=d'


def create_session(cookie=None):
    cookie = cookie or wd_cookie
    session = requests.Session()
    session.mount("https://", requests.adapters.HTTPAdapter(max_retries=1))
    headers = {
        'Cookie': cookie,
        'User-Agent': 'game=KiwiGame, engine=UE4, version=0',
        'Host': 'api.prod.capcomfighters.net',
        'Connection': 'Keep-Alive',
        'Cache-Control': 'no-cache',
    }
    session.headers.update(headers)
    return session


def query_cookie_status(session):
    url = LICENSE_URL % ("%s", "")
    res = query_cfn(session, url)
    cd = save_cookie_status(res)
    return cd, res


def get_cookie_status(session):
    cd = load_cookie_status()
    if cd is None or cd.is_old():
        cd, _ = query_cookie_status(session)
    return cd


def test_cookie_status(session):
    if get_cookie_status(session).is_invalid:
        send_error_message("test_cookie_status failed")
        raise CookieInvalidException


def query_cfn(session, url):
    cookie = session.headers['Cookie']
    req_number = cookie.split('%3A')[0].split('=')[1]
    req_url = 'https://api.prod.capcomfighters.net%s' % (url % req_number)
    response = session.get(req_url, verify=False)
    return response


def record_top_players(session):
    ranking_results = []
    for i in range(1, 11):
        url = RANKING_URL % ('%s', i)
        rank_response = query_cfn(session, url)
        if rank_response.status_code != 200:
            raise Exception
        rank_data = rank_response.json()['response'][0]['rankingresult']
        ranking_results.extend(rank_data)
    save_ranking_results(ranking_results)


def _query_player_match_history(session, pid):
    url = MATCH_URL % ('%s', pid)
    res = query_cfn(session, url)
    if res.status_code != 200:
        log("got a non-200 response:\n%s" % res.text)
        raise MatchQueryException()
    try:
        match_results = res.json()['response'][0]['matchresults']
    except Exception as e:
        log_exception(e)
        log('failed to extract json, dumping res:\n%s' % res.text)
        raise MatchQueryException()
    else:
        return match_results


def _bulk_query_match_history(session, pids):
    match_list = []
    count = 1
    total = len(pids)
    player_matches = {}
    is_error = False
    for pid in pids:
        log("Fetching match history for %s (%s/%s)" % (pid, count, total))
        count += 1
        try:
            matches = _query_player_match_history(session, pid)
        except MatchQueryException:
            # pretend we got 0 matches so that player gets marked as "updated"
            # this prevents a bunch of bad players from starving the rest
            matches = []
            is_error = True
        match_list.extend(matches)
        player_matches[pid] = matches
    return is_error, match_list, player_matches


def batch_query_match_history(session, pids):
    pids_list = list(pids)
    total = len(pids_list)
    batch = 50
    player_matches = {}
    any_error = False
    log("Begin querying %s players" % total)
    for idx in range(0, total, batch):
        next_idx = idx + batch
        bound = next_idx if next_idx < total else total
        sub_pids = pids_list[idx:bound]
        log('Attempting to query players %s-%s of %s' % (idx, bound, total))
        is_error, matches, player_matches_dict = _bulk_query_match_history(
            session, sub_pids
        )
        any_error = any_error or is_error
        save_match_list(matches)
        player_matches.update(player_matches_dict)
    set_player_updated_at(player_matches.keys())
    with DATABASE.atomic():
        cache = MatchCache()
        for pid, matches in player_matches.items():
            cache.process_matches(pid, matches)
        cache.save()
    return any_error


def fix_player_names(session):
    players = (
        Player
        .select()
        .where(Player.name == '')
    )
    player_ids = [p.cfn_id for p in players]
    log("found %s players with missing names" % len(player_ids))

    if len(player_ids) == 0:
        return
    for pid in player_ids:
        url = LICENSE_URL % ('%s', pid)
        res = query_cfn(session, url)
        try:
            new_name = res.json()['response'][0]['displayid']
        except json.decoder.JSONDecodeError as e:
            log(res.text)
            raise e
        log('%s -> %s' % (pid, new_name))
        (
            Player
            .update(name=new_name)
            .where(Player.cfn_id == pid)
            .execute()
        )

PROBLEM_CHARS = frozenset('_')


def _query_rival(session, query_name, player_name):
    url = RIVAL_URL % ('%s', query_name)
    res = query_cfn(session, url)
    matching_players = res.json()['response'][0]['searchresult']
    for player in matching_players:
        cfn_model = CFNPlayerSearchModel(player)
        log('logging cfn player')
        log(cfn_model.__dict__)
        if cfn_model.name.lower() == player_name.lower():
            subscribe_to_new_player(cfn_model)
            return cfn_model.name
    return None


def add_player_by_name(session, player_name):
    test_cookie_status(session)  # might raise
    query_names = [player_name]
    for pc in PROBLEM_CHARS:
        if pc in player_name:
            query_names.extend(player_name.split(pc))
    for qn in query_names:
        res = _query_rival(session, qn, player_name)
        if res:
            return res
    return None
