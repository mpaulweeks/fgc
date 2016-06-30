#!/usr/bin/env python3

from playhouse.csv_loader import load_csv

from py.src.logger import log
from py.src.settings import (
    ENVARS,
    DATABASE,
)
from py.src.db.model import (
    Player,
    Rank,
    Match,
)


def create_demo_db():
    if not ENVARS.is_demo_web_server():
        raise Exception('wrong database! call this again with FGC_DEMO_DB=1')
    DATABASE.create_tables([Player, Match, Rank])
    load_csv(Rank, 'temp/rank.csv')
    load_csv(Player, 'temp/player.csv')


def main():
    log('creating demo db from csv files')
    create_demo_db()
