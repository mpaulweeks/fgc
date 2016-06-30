# FightingGame.Community

This is the source code for [fightinggame.community](http://fightinggame.community).

See also: [fgc-status](https://github.com/mpaulweeks/fgc-status)

## About

This repository is not actively maintained, nor was it built with open-source in mind.

I have provided it here for those who are curious and want to tinker with the CFN api.

I have hastily made some last minute docs to document how to get this running. [Setting up the demo](demo/README.md) is a great place to start.

If you want to start poking around the CFN api, I suggest you start reading these files (more docs to follow):
- [script for establishing cookie associated with your server's IP](shell/register_cookie.sh)
- [how to store your cookie so the code uses it](local/README.md)
- [communicating with CFN's api](py/src/cfn/api.py)
- [parsing CFN's objects](py/src/match/model/cfn.py)
- [character IDs and other related info](py/src/cfn/cfn_constants.py)

## License

MIT
