#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
import json
from py.src.logger import log
from py.src.error import (
    PlayerDoesNotExist,
)
from py.src.db.model import (
    LowerStr,
    Match,
    Player,
    Rank,
)
from py.src.db.api import (
    bulk_insert,
)
from py.src.s3_store import (
    load_global_cache_from_file,
    save_global_cache_dict_to_file,
)


def _get_now_str():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


class PlayerRanking():

    def __init__(self, player, rank):
        self.player_cfn_id = rank.player_cfn_id
        self.placement = rank.placement
        self.name = player.name
        self.league_points = rank.league_points
        self.created_at = rank.created_at
        self.region = player.region
        self.platform = player.platform
        self.favorite_character_id = rank.favorite_character
        self.most_used_character_id = player.match_character


def load_player_rankings():
    latest = (
        Rank
        .select(Rank.created_at)
        .order_by(Rank.created_at.desc())
        .scalar()
    )
    ranks = (
        Rank
        .select(Rank, Player)
        .join(Player)
        .where(Rank.created_at == latest)
    )
    return [PlayerRanking(r.player_cfn, r) for r in ranks]


def _insert_missing_players(player_source):
    log("determining missing players")
    player_source_ids = [ps['cfn_id'] for ps in player_source]
    existing_pids, missing_pids = (
        _determine_missing_cfn_ids(Player, player_source_ids)
    )
    missing_players = [
        ps for ps in player_source
        if ps['cfn_id'] in missing_pids
    ]
    log("inserting missing players")
    bulk_insert(Player, missing_players)
    return existing_pids


def _insert_missing_matches(match_source):
    log("determining missing matches")
    match_source_ids = [ms['cfn_id'] for ms in match_source]
    existing_mids, missing_mids = (
        _determine_missing_cfn_ids(Match, match_source_ids)
    )
    missing_matches = [
        ms for ms in match_source
        if ms['cfn_id'] in missing_mids
    ]
    log("inserting missing matches")
    bulk_insert(Match, missing_matches)


def save_ranking_results(ranking):
    player_source = [
        {
            'cfn_id': int(rank['pidx']),
            'name': rank['userid'],
            'subscribed': 0,
            'region': rank['region'],
            'platform': rank['accountsource'],
        } for rank in ranking
    ]
    existing_pids = _insert_missing_players(player_source)

    rank_source = [
        {
            'player_cfn': int(rank['pidx']),
            'league_points': int(rank['lp']),
            'placement': int(rank['rownum']),
            'favorite_character': int(rank['favchar']),
        } for rank in ranking
    ]
    bulk_insert(Rank, rank_source)

    player_ids = [r['player_cfn'] for r in rank_source]
    set_subscribed(player_ids)

    player_update = [
        {
            'cfn_id': int(rank['pidx']),
            'region': rank['region'],
            'platform': rank['accountsource'],
        } for rank in ranking
        if int(rank['pidx']) in existing_pids
    ]
    regions = defaultdict(set)
    platforms = defaultdict(set)
    for pu in player_update:
        regions[pu['region']].add(pu['cfn_id'])
        platforms[pu['platform']].add(pu['cfn_id'])
    for region, pids in regions.items():
        (
            Player
            .update(region=region)
            .where((Player.region >> None) & (Player.cfn_id << list(pids)))
            .execute()
        )
    for platform, pids in platforms.items():
        (
            Player
            .update(platform=platform)
            .where((Player.platform >> None) & (Player.cfn_id << list(pids)))
            .execute()
        )


def load_player_by_name(name):
    try:
        return (
            Player
            .get(Player.name == name, Player.subscribed == 1)
        )
    except Player.DoesNotExist:
        raise PlayerDoesNotExist()


def load_player_by_id(player_id):
    try:
        return (
            Player
            .get(Player.cfn_id == player_id)
        )
    except Player.DoesNotExist:
        raise PlayerDoesNotExist()


def load_player_by_approx_name(name):
    try:
        return (
            Player
            .get(LowerStr(Player.name) == name.lower())
        )
    except Player.DoesNotExist:
        raise PlayerDoesNotExist()


def load_subscribed_player_names():
    daos = (
        Player
        .select(Player.name)
        .where(Player.subscribed == 1)
    )
    return set([
        p.name for p in daos
    ])


def load_subscribed_player_ids(
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
            .order_by(Player.updated_at)
            .limit(batch_size)
        )
    return set([
        p.cfn_id for p in query
    ])


def load_player_ids_to_backfill(
        subset_ids=None,
        batch_size=None,
        ):
    query = (
        Player
        .select()
        .where(Player.subscribed == 1)
        .where(~(Player.updated_at >> None))
    )
    if subset_ids:
        query = (
            query
            .where(Player.cfn_id << list(subset_ids))
        )
    if batch_size:
        query = (
            query
            .order_by(Player.match_updated_at)
            .limit(batch_size)
        )
    return set([
        p.cfn_id for p in query
    ])


def load_player_ticks():
    return list(
        Player
        .select(Player.cfn_id, Player.match_latest_ticks)
        .where(Player.subscribed == 1)
    )


def subscribe_to_new_player(player_model):
    existing = (
        Player
        .select()
        .where(Player.cfn_id == player_model.cfn_id)
    )
    if existing:
        (
            Player
            .update(
                subscribed=1,
                name=player_model.name,
                region=player_model.region,
                platform=player_model.platform,
            )
            .where(Player.cfn_id == player_model.cfn_id)
            .execute()
        )
    else:
        bulk_insert(Player, [{
            'cfn_id': player_model.cfn_id,
            'name': player_model.name,
            'region': player_model.region,
            'platform': player_model.platform,
            'subscribed': 1,
        }])


def save_match_list(match_list):
    log("arranging fetched data")
    matches = dict()
    for match in match_list:
        mid = int(match['matchid'])
        matches[mid] = match

    log("processing matches")
    match_source = [
        {
            'cfn_id': mid,
            'left_player_cfn_id': int(match['leftstartplayer']),
            'right_player_cfn_id': int(match['rightstartplayer']),
            'data': json.dumps(match),
        } for mid, match in matches.items()
    ]
    _insert_missing_matches(match_source)


def save_player_cache(player):
    player.save()


def set_subscribed(pids):
    log("updating affected players to subscribed")
    if not pids:
        return
    (
        Player
        .update(subscribed=1)
        .where(Player.subscribed == 0, Player.cfn_id << list(pids))
        .execute()
    )


def set_player_updated_at(pids):
    log("setting players as updated")
    if not pids:
        log('no players to update!')
        return
    now_str = _get_now_str()
    (
        Player
        .update(updated_at=now_str)
        .where(Player.cfn_id << list(pids))
        .execute()
    )


def _determine_missing_cfn_ids(model, all_ids):
    if not all_ids:
        return set(), set()
    existing_models = (
        model
        .select(model.cfn_id)
        .where(model.cfn_id << list(all_ids))
    )
    existing_ids = set([model.cfn_id for model in existing_models])
    missing_ids = set(all_ids) - existing_ids
    return existing_ids, missing_ids


def get_latest_player_updated_at():
    return (
        Player
        .select()
        .order_by(Player.updated_at.desc())
        .get()
    ).updated_at


def get_subscribed_player_count():
    return (
        Player
        .select()
        .where(Player.subscribed == 1)
        .count()
    )


def load_ranked_match_cache():
    cache_dict = load_global_cache_from_file()
    return cache_dict


def save_global_ranked_match_cache(global_data):
    global_match_dict = global_data.to_dict()
    save_global_cache_dict_to_file(global_match_dict)
