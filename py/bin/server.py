#!/usr/bin/env python3

import os
import subprocess
import threading

from py.src.bottle import (
    Bottle,
    abort,
    response,
    request,
    run,
    template,
    view,
    static_file,
)

from py.src.logger import log
from py.src.repo import (
    get_number_of_subscribed_players,
    get_subscribed_player_names,
    search_player_by_name,
    subscribe_to_player,
)
from py.src.cfn.api import (
    create_session,
    add_player_by_name,
    get_cookie_status,
)
from py.src.error import (
    PlayerDoesNotExist,
    CookieInvalidException,
)
from py.src.settings import (
    ENVARS,
    DATABASE,
)
from py.src.view_model import (
    LeaderboardViewModel,
    PlayerViewModelCache,
    GlobalViewModelCache,
)


bottle_web = Bottle()
bottle_api = Bottle()

PROCESS_ID = os.getpid()

_cache_player_names = None
_cache_player_rankings = None
_cache_player_stats = None
_cache_global_stats = None


def _setup_base():
    with open('temp/server.pid', 'wt') as f:
        f.write(str(PROCESS_ID))


def setup_web():
    _setup_base()
    _open_db_conn()
    _refresh_cache()
    _close_db_conn()


def setup_api():
    _setup_base()


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        origin = request.get_header('Origin', default='')
        if not origin.endswith('fightinggame.community'):
            origin = 'http://fightinggame.community'
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = (
            'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        )

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)
    return _enable_cors


def _kill_server():
    os._exit(0)


@bottle_api.hook('before_request')
@bottle_web.hook('before_request')
def _open_db_conn():
    DATABASE.connect()


@bottle_api.hook('after_request')
@bottle_web.hook('after_request')
def _close_db_conn():
    if not DATABASE.is_closed():
        DATABASE.close()


@bottle_web.get('/favicon.ico')
def static_favicon():
    return static_file('favicon.ico', root='static/img')


@bottle_web.get('/static/css/<filename>')
def static_css(filename):
    return static_file(filename, root='static/css')


@bottle_web.get('/static/img/<filename>')
def static_img(filename):
    return static_file(filename, root='static/img')


@bottle_web.get('/static/js/<filename>')
def static_js(filename):
    return static_file(filename, root='static/js')


def _get_player_names():
    return _cache_player_names


def _get_player_rankings():
    return _cache_player_rankings


def _get_global_character_matchups(
        p1_league_codes=None,
        p2_league_codes=None):
    return _cache_global_stats.get_by_leagues(
        p1_league_codes or [],
        p2_league_codes or [],
    )


def _get_player_by_name(player_name):
    try:
        return _cache_player_stats.get_by_name(player_name)
    except PlayerDoesNotExist:
        return None


def _refresh_cache():
    global _cache_player_names
    global _cache_player_rankings
    global _cache_player_stats
    global _cache_global_stats
    _cache_player_names = get_subscribed_player_names()
    _cache_player_rankings = LeaderboardViewModel()
    _cache_player_stats = PlayerViewModelCache()
    _cache_global_stats = GlobalViewModelCache()


@bottle_web.get('/')
@view('welcome')
def index():
    return {
        "title": "FightingGame.Community",
    }


@bottle_web.get('/matchup')
@view('player')
def matchup():
    p1_league_codes = request.query.getall('player')
    p2_league_codes = request.query.getall('opponent')
    global_vm = _get_global_character_matchups(
        p1_league_codes, p2_league_codes
    )
    return {
        "title": "Character Matchups",
        "vm": global_vm,
    }


@bottle_web.get('/player')
@view('player_lookup')
def player_lookup():
    return {
        "player_names": _get_player_names(),
    }


@bottle_web.get('/player/<player_name>')
@view('player')
def player(player_name):
    player_vm = _get_player_by_name(player_name)
    if player_vm is None:
        return template(
            'player_not_found',
            **{"player_names": _get_player_names()}
        )
    return {
        "title": player_name,
        "vm": player_vm,
    }


@bottle_web.get('/new_player')
@view('new_player')
def new_player():
    return {
        "api_host": ENVARS.api_host,
    }


@bottle_web.get('/about')
@view('about')
def about():
    return {
    }


@bottle_web.get('/goodbye')
@view('goodbye')
def goodbye():
    return {
        'is_goodbye': True,
    }


@bottle_web.get('/leaderboard')
@view('leaderboard')
def leaderboard():
    player_rankings_vm = _get_player_rankings()
    return {
        "vm": player_rankings_vm,
    }


@bottle_web.get('/admin/status/pid')
@bottle_api.get('/admin/status/pid')
def get_pid():
    return (str(PROCESS_ID))


@bottle_web.route('/admin/status/web', method=['OPTIONS', 'GET'])
@bottle_api.route('/admin/status/web', method=['OPTIONS', 'GET'])
@enable_cors
def healthcheck():
    process_status = subprocess.check_output(
        ["./shell/mem_check.sh"],
    )
    return ("%s" % str(process_status))


@bottle_api.route('/admin/status/cfn', method=['OPTIONS', 'GET'])
@enable_cors
def check_cookie():
    with create_session() as session:
        cd = get_cookie_status(session)
    if cd.is_invalid:
        abort(500, "Connection Expired")
    return 'ok'


@bottle_web.get('/admin/status/data')
@bottle_api.get('/admin/status/data')
@enable_cors
def check_data():
    num_subbed = get_number_of_subscribed_players()
    message = ('%s players currently subscribed' % num_subbed)
    return message


@bottle_web.post('/admin/invalidate_cache')
def invalidate_cache():
    _refresh_cache()
    log('cache refreshed')
    return


@bottle_api.delete('/admin/kill/<process_id>')
@bottle_web.delete('/admin/kill/<process_id>')
def shut_down(process_id):
    if process_id == str(PROCESS_ID):
        log('signal received! shutting down...')
        with open('temp/server.pid', 'wt') as f:
            f.write('')
        threading.Timer(1, lambda: _kill_server()).start()
        return 'killed: %s' % PROCESS_ID
    else:
        log('nice try: %r != %r' % (process_id, PROCESS_ID))
        abort(404)


@bottle_api.route('/sfv/new_player/<player_name>', method=['OPTIONS', 'POST'])
@enable_cors
def new_player_submit(player_name):
    is_new = False
    is_error = False
    try:
        found_player = search_player_by_name(player_name)
        fixed_name = found_player.name
        if not found_player.subscribed:
            subscribe_to_player(found_player.cfn_id)
            is_new = True
    except PlayerDoesNotExist:
        with create_session() as session:
            try:
                fixed_name = add_player_by_name(session, player_name)
            except CookieInvalidException:
                fixed_name = None
                is_error = True
        is_new = True
    return {
        'player_name': fixed_name,
        'is_new': is_new,
        'is_error': is_error,
        'is_match': fixed_name is not None,
    }


def start_server():
    if ENVARS.is_web_testing:
        bottle_web.merge(bottle_api)
    if ENVARS.is_web_server():
        designated_bottle_app = bottle_web
        designated_setup = setup_web
    elif ENVARS.is_api_server():
        designated_bottle_app = bottle_api
        designated_setup = setup_api
    else:
        log('no webserver for instance type: %s' % ENVARS.instance_type)
        return
    designated_setup()
    run(
        designated_bottle_app,
        server='cherrypy',
        host='localhost',
        port=5555,
        debug=ENVARS.debug,
    )

if __name__ == "__main__":
    start_server()
