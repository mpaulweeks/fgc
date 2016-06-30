#!/bin/sh
FGC_WEB_TEST=1 FGC_API_HOST=localhost:5555 python3 -m py.test.test_server
