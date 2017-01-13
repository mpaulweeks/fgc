# FightingGame.Community

This is the source code for [fightinggame.community](http://fightinggame.community), which has suspended development.

The website provided statistics for Street Fighter V by crawling the Capcom Fighters Network (CFN) api.

See also: [fgc-status](https://github.com/mpaulweeks/fgc-status)

## About

This repository is not actively maintained, nor was it built to be an open-source library.

I have provided it here for those who are curious and want to tinker with the CFN api.

In the process of coding this website, I re-invented a couple of wheels (deploy tools, testing, logging) as a learning exercise. If you wish to fork this repo and expand on it, I highly recommend you just keep the main python logic and replace the rest with standard libraries.

I have hastily made some last minute docs on how to get this running as is: [Setting up the demo](demo/README.md)

If you want to start poking around the CFN api, I suggest you start reading these files (more docs to follow):
- [script for establishing cookie associated with your server's IP](shell/register_cookie.sh)
- [how to store your cookie so the code uses it](local/README.md)
- [communicating with CFN's api](py/src/cfn/api.py)
- [parsing CFN's objects](py/src/match/model/cfn.py)
- [character IDs and other related info](py/src/cfn/cfn_constants.py)

## FAQ

__How do I get the cookie?__

I used a manual process wherein I authenticated using the game client, while sniffing the traffic for time-sensitive login information, and then used those credentials to repeat the login request on my crawler server, thereby gaining a cookie that would work on that machine (the cookie's appear to track IP, so each server has to sign itself in).

This is how I did it:

1. Get the website code set up on a server.
2. Launch SFV on a PC, use Fiddler or Wireshark (or equivalent program) to monitor HTTPS traffic, find the call that logs in your game client, copy out the "authcode" argument in the POST request body.
3. Run the "register_cookie.sh" script on the server, when it prompts for authcode, paste the value you copied from above. You should get back a response that contains a cookie.
4. Add that cookie to the "local/envar.json" of the server, eg: `"FGC_SCRAPER_COOKIE": "binf=289479238447;"`
5. Use the server to periodically crawl the api and store the data for later reading in a database.

If you ever want to make dynamic API requests from any device without setup (ie like a mobile app), you would need to first reverse-engineer how the SFV game client generates those "authcode" values. As mentioned above, the login cookies are IP-specific so you can't just login once and then pass it around.

## License

MIT
