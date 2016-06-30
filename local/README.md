# local/

This is a placeholder directory whose contents are ignored by git.

This directory is meant to store files that are either security-related or could be out-of-date w/r/t other servers.

Files expected for server operation:
- `envar.json`
- `global_cache.json`
- `demo.db` if running the demo web server

See `demo/` directory for sample files.

Example `envar.json` for a scraping server (with sensitive values emptied):
```
{
    "FGC_SCRAPER_COOKIE": "",
    "FGC_MANUAL_TEST_COOKIE": "",
    "CURRENT_ENV_COOKIE": "FGC_SCRAPER_COOKIE", // selects which cookie to use
    "DB_HOST": "",
    "DB_USERNAME": "",
    "DB_PASSWORD": "",
    "DB_DATABASE_NAME": "",
    "DB_PORT": 0,
    "aws_access_key_id": "",
    "aws_secret_access_key": "",
    "s3_region_name": "",
    "s3_bucket_name": "",
    "mailgun_api_key": "",
    "mailgun_domain_name": "",
    "mailgun_recipient": "",
    "instance_type": "scraper", // determines setup, valid choices = ['web', 'api', 'scraper', 'dev', 'demo']
    "server_name": "scraper-1", // for logging
    "DEBUG": false
}
```
