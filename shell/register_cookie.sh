#!/bin/sh
read -p "Enter POST arguments:" blob
curl -v -k -X POST -A 'game=KiwiGame, engine=UE4, version=0' --cookie 'einf=WindowsNoEditor%3A9841082371%3A3232235791%3A0%3A0%3A0%3A0%3Aen_US; ' 'https://api.prod.capcomfighters.net/login/extlogin.php' --data $blob
