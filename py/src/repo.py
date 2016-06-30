#!/usr/bin/env python3

from py.src.logger import log
from py.src.store import (
    get_subscribed_player_count,
    load_ranked_match_cache,
    load_subscribed_player_names,
    load_player_by_approx_name,
    load_player_by_name,
    load_player_rankings,
    load_player_ticks,
    set_subscribed,
)


def get_subscribed_player_names():
    return load_subscribed_player_names()


def get_player_by_name(player_name):
    return load_player_by_name(player_name)


def get_global_ranked_match_cache():
    return load_ranked_match_cache()


def get_player_ticks():
    players = load_player_ticks()
    ticks = {p.cfn_id: p.match_latest_ticks for p in players}
    return ticks


def get_player_rankings():
    return load_player_rankings()


def get_number_of_subscribed_players():
    return get_subscribed_player_count()


def search_player_by_name(player_name):
    return load_player_by_approx_name(player_name)


def subscribe_to_player(player_id):
    set_subscribed([player_id])
