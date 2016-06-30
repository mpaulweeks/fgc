#!/bin/sh
python3 -m py.bin.load_crontab

./shell/restart_server.sh
