# NOTES

Misc notes I took during the development process.

## links/resources
* [datatables](http://datatables.net/)
* [bootstrap-select](https://silviomoreto.github.io/bootstrap-select/)
* [nginx custom error](http://nginxlibrary.com/403-forbidden-error/)

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
