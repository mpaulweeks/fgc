# FightingGame.Communtiy

## links/resources
* [datatables](http://datatables.net/)
* [bootstrap-select](https://silviomoreto.github.io/bootstrap-select/)
* [nginx custom error](http://nginxlibrary.com/403-forbidden-error/)

## installation on ec2
* `sudo yum install git`
* Clone git repo w/ password
* `cd cfn && ./install/ec2.sh`
* Fill `local/envar.json`
* `python3 -m py.bin.task_download_cache`
* generate CFN cookie
* `./shell/on_reload.sh`

## data/external assumptions
* cfn player/match ids are unique
* match ticks can be trusted
* player names are unique
* players will never be deleted

## services

### fgc-web
* webserver: YES
* cfn cookie: NO
* db: READ
* s3: READ

### fgc-api
* webserver: YES
* cfn cookie: YES
* db: WRITE
* s3: N/A

### fgc-scraper
* webserver: NO
* cfn cookie: YES
* db: WRITE
* s3: WRITE

### fgc-demo
* webserver: YES
* cfn cookie: NO
* db: N/A
* s3: N/A
