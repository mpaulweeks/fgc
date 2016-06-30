#!/usr/bin/env python3

from peewee import *
from playhouse.pool import PooledMySQLDatabase

from py.src.logger import log
from py.src.settings.envar import (
    ENVARS,
)

# imported by other modules
DATABASE = None


def demo_database():
    log('connecting to local demo db')
    return SqliteDatabase('local/demo.db')


def prod_database():
    log('connecting to prod db')
    return PooledMySQLDatabase(
        ENVARS.database_name,
        host=ENVARS.host,
        user=ENVARS.username,
        password=ENVARS.password,
        max_connections=32,  # 50 max on t2.micro
        stale_timeout=300,  # 5 minutes.
    )


def test_temp_database():
    log('connecting to in-memory test db')
    return SqliteDatabase(':memory:')


def test_local_database():
    log('connecting to local test db')
    return SqliteDatabase('local/test.db')


if ENVARS.is_unit_testing:
    DATABASE = test_temp_database()
elif ENVARS.is_web_testing:
    DATABASE = test_local_database()
elif ENVARS.is_demo_web_server():
    DATABASE = demo_database()
else:
    DATABASE = prod_database()
