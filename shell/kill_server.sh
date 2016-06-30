#!/bin/sh
# this is idempotent and safe to run on non-web instances
pid=$(cat temp/server.pid)
curl -v -X DELETE "http://localhost:5555/admin/kill/$pid"
