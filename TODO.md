# TODO

## plan for de-centralized crawling
* add column to match table "processed_at"
* normal match pulling/updated at is unaffected, new matches have processed_at=null
* match pulling is distributed across many machines
* single "cruncher" machine periodically checks for new matches, updates players/global, then sets matches as processed
* no conditions on processing matches, do away with old system of latest_match_id
* to save space, old processed matches can have their response column set to null

## misc todo
* explore idea of pulling most users on-demand (when their page is loaded)
* make error logger a "with" wrapper?
    * sends email on close if exiting block abnormally or state altered
* find long term solution for match table
    * when pulling matches and saving to db, only save if time > player ticks
    * migrate to archive based on match ticks
        * add new column to match, backfill gradually
* improve player lookup page/dropdown
* explicit setup-everything script (python, uses envar)
* cron to simulate status page, email me if anything down
* integration tests against temp db
* remove all un-subscribed players, remove subscribed field?
    * meh, non-urgent
* ween/combine player.updated_at and player.match_updated_at
* dynamically disable adding players if cookie gooes down? store status in db?
* async the cfn requests
