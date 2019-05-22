#!/usr/bin/env bash

## Install python and OS-level dependencies
apt-get install -y python3 python3-pip python-dev


cd /autograder/source


## Deal with deploy key and ssh settings
SSH_DIR="ssh"
mkdir -p /root/.ssh
cp $SSH_DIR/ssh_config /root/.ssh/config
chmod 600 $SSH_DIR/deploy_key  # fix file permissions issue requiring private key to be inaccessible to other users on the filesystem
cp $SSH_DIR/deploy_key /root/.ssh/deploy_key
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts # Prevent host key verification errors at runtime


## Pull updates from git
source update.sh
