#!/usr/bin/env python3

from peewee import *
import json

from py.src.logger import log
from py.src.settings import (
    DATABASE,
)

LowerStr = fn.Lower


class BaseModel(Model):
    class Meta:
        database = DATABASE

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return self.__str__()


class Player(BaseModel):
    cfn_id = BigIntegerField(primary_key=True)
    name = CharField()
    subscribed = IntegerField(default=0)
    updated_at = DateTimeField(null=True)
    region = CharField(null=True)
    platform = CharField(null=True)
    match_updated_at = DateTimeField(null=True)
    match_latest_ticks = IntegerField(null=True)
    match_data = TextField(null=True)
    match_character = IntegerField(null=True, default=None)

    class Meta:
        db_table = 'player'

    def get_match_cache(self):
        cache_json = self.match_data
        cache_dict = json.loads(cache_json) if cache_json else None
        return cache_dict


class Match(BaseModel):
    cfn_id = BigIntegerField(primary_key=True)
    data = TextField()
    left_player_cfn_id = BigIntegerField()
    right_player_cfn_id = BigIntegerField()

    class Meta:
        db_table = 'match'


class Rank(BaseModel):
    created_at = DateTimeField()
    id = BigIntegerField(primary_key=True)
    league_points = IntegerField()
    placement = IntegerField()
    player_cfn = ForeignKeyField(
        db_column='player_cfn_id',
        rel_model=Player,
        to_field='cfn_id',
    )
    favorite_character = IntegerField()

    class Meta:
        db_table = 'rank'
