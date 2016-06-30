# demo/

Installing the demo on fresh ec2 instance:
```
sudo yum install git
git clone https://github.com/mpaulweeks/fgc.git
cd fgc
git checkout deploy
git pull
unzip demo/local.zip -d local/
./install/ec2.sh
./shell/on_reload.sh
sudo yum install nginx
sudo cp install/nginx/nginx.conf /etc/nginx/nginx.conf
sudo cp install/nginx/fgc_web.conf /etc/nginx/conf.d/fgc_web.conf
sudo service nginx restart
```