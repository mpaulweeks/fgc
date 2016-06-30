#!/bin/sh

gout=$(git pull 2>&1)
echo $gout
if ! [[ $gout == *"Already up-to-date." ]]
then
  echo "Changes found, firing reload..."
  ./shell/on_reload.sh
fi
