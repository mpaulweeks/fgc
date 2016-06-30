#!/usr/bin/env python3

from py.src.logger import log
from py.src.settings import (
    ensure_testing,
    DATABASE,
)
from py.src.db.model import (
    Match,
    Player,
    Rank,
)


def ensure_test_tables():
    ensure_testing()
    if not Player.table_exists():
        log('creating test tables')
        DATABASE.create_tables([Player, Match, Rank])


def bulk_insert(model, data_source):
    total = len(data_source)
    batch = 1000
    log("Trying to insert %s rows" % total)
    with DATABASE.atomic():
        for idx in range(0, total, batch):
            (
                model
                .insert_many(data_source[idx:idx + batch])
                .execute()
            )
            log("Inserted %s" % (idx + batch))
