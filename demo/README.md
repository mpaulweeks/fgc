# demo/

## Installing the demo on ec2
- `sudo yum install git`
- `git clone https://github.com/mpaulweeks/fgc.git`
- `cd fgc && ./install/ec2.sh`
- `unzip demo/local.zip -d local/`
- `git checkout deploy && git pull`
- `./shell/on_reload.sh`
