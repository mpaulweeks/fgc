#!/usr/bin/env python3

import json
from py.src.time_util import (
    convert_dt_to_seconds,
)
from py.src.settings import (
    ENVARS,
)

wd_cookie = ENVARS.cookie
_TEMP_COOKIE_FILE = 'temp/cookie_response.json'


class CookieData():

    def __init__(self, updated_at_seconds, response_text):
        self.updated_at_seconds = updated_at_seconds
        self.response_text = response_text

    def to_file(self, cookie_file):
        json.dump(self.__dict__, cookie_file)

    def is_old(self):
        return (
            300 < CookieData.utcnow_seconds() - self.updated_at_seconds
        )

    @property
    def is_invalid(self):
        return (
            "Session Expired" in self.response_text or
            "session error" in self.response_text
        )

    @staticmethod
    def from_file(cookie_file):
        json_data = json.load(
            cookie_file,
        )
        return CookieData(
            json_data['updated_at_seconds'],
            json_data['response_text'],
        )

    @staticmethod
    def utcnow_seconds():
        return convert_dt_to_seconds()

    @staticmethod
    def from_response(response):
        return CookieData(
            CookieData.utcnow_seconds(),
            response.text,
        )


def load_cookie_status():
    try:
        with open(_TEMP_COOKIE_FILE) as f:
            return CookieData.from_file(f)
    except FileNotFoundError:
        pass
    return None


def save_cookie_status(response):
    cd = CookieData.from_response(response)
    with open(_TEMP_COOKIE_FILE, 'w') as f:
        cd.to_file(f)
    return cd
