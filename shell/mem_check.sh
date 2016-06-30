#!/bin/sh
ps -p `cat temp/server.pid` -o %cpu,%mem,cmd