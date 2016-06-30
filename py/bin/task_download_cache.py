#!/usr/bin/env python3

from py.src.logger import log
from py.src.s3_store import (
    download_global_cache,
)


def main():
    download_global_cache()


if __name__ == "__main__":
    main()
