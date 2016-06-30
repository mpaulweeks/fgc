
from datetime import (
    datetime,
    timedelta,
)
from py.src.logger import log


def convert_dt_to_seconds(dt=None):
    dt = dt or datetime.utcnow()
    return (
        dt - datetime(1970, 1, 1)
    ).total_seconds()


def convert_dt_to_nyc(dt=None):
    dt = dt or datetime.utcnow()
    if dt is None:
        return None
    updated_time = dt - timedelta(hours=5)
    # cheap shitty utc conversion
    return updated_time.strftime("%Y-%m-%d")


def convert_ticks_to_nyc(raw_ticks):
    if raw_ticks is None:
        return None
    ticks = raw_ticks/10
    updated_time = (
        datetime(1, 1, 1) +
        timedelta(microseconds=ticks)
    )
    return convert_dt_to_nyc(updated_time)
