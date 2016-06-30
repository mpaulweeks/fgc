#!/bin/sh
> nohup.out
./shell/kill_server.sh
sleep 2
./shell/background_server.sh
