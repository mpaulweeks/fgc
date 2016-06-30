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

## License

MIT
