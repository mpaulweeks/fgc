#!/usr/bin/env python3

import json
import os

from py.src.error import (
    TestingException,
)


def _load_envars():
    try:
        with open('local/envar.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data


def ensure_not_testing():
    if ENVARS.is_testing():
        raise TestingException()
    return True


def ensure_testing():
    if not ENVARS.is_testing():
        raise TestingException()
    return True


INSTANCE_DEV = "dev"
INSTANCE_WEB = "web"
INSTANCE_DEMO = "demo"
INSTANCE_API = "api"
INSTANCE_SCRAPER = "scraper"
INSTANCE_TYPES = frozenset([
    INSTANCE_DEV,
    INSTANCE_WEB,
    INSTANCE_DEMO,
    INSTANCE_API,
    INSTANCE_SCRAPER,
])


class _ENVARS():

    def __init__(self, data):
        self.cookie = data.get(data.get("CURRENT_ENV_COOKIE"))
        self.host = data.get("DB_HOST")
        self.username = data.get("DB_USERNAME")
        self.password = data.get("DB_PASSWORD")
        self.database_name = data.get("DB_DATABASE_NAME")
        self.port = data.get("DB_PORT")
        self.aws_access_key_id = data.get("aws_access_key_id")
        self.aws_secret_access_key = data.get("aws_secret_access_key")
        self.s3_region_name = data.get("s3_region_name")
        self.s3_bucket_name = data.get("s3_bucket_name")
        self.mailgun_api_key = data.get("mailgun_api_key")
        self.mailgun_domain_name = data.get("mailgun_domain_name")
        self.mailgun_recipient = data.get("mailgun_recipient")
        self.server_name = data.get("server_name", "unknown")
        self.instance_type = data.get("instance_type", INSTANCE_DEV)
        if self.instance_type not in INSTANCE_TYPES:
            self.instance_type = INSTANCE_DEV

        # optional/local/test settings
        self.debug = data.get("DEBUG", False)
        self.is_unit_testing = bool(os.getenv("FGC_UNIT_TEST", False))
        self.is_web_testing = bool(os.getenv("FGC_WEB_TEST", False))
        self.api_host = os.getenv("FGC_API_HOST", "api.fightinggame.community")

    def is_testing(self):
        return self.is_unit_testing or self.is_web_testing

    def is_demo_web_server(self):
        return self.instance_type == INSTANCE_DEMO

    def is_web_server(self):
        return self.instance_type in [
            INSTANCE_DEV,
            INSTANCE_WEB,
            INSTANCE_DEMO,
        ]

    def is_api_server(self):
        return self.instance_type == INSTANCE_API

ENVARS = _ENVARS(_load_envars())
