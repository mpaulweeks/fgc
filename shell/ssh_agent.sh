#!/bin/sh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
ssh -T git@bitbucket.org