#!/usr/bin/env python3

from py.src.logger import log
from py.src.cfn.api import (
    create_session,
    query_cookie_status,
)


def main():
    with create_session() as session:
        cd, res = query_cookie_status(session)
        log(res.status_code)
        log(res.headers)
        log(res.text)
        log("cookie is good: %s" % (not cd.is_invalid))

if __name__ == "__main__":
    main()
