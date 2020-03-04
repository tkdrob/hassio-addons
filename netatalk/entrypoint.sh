#!/bin/bash

CONFIG_PATH=/data/options.json
AFP_USER=$(jq --raw-output ".afp_username" $CONFIG_PATH)
AFP_PASSWORD=$(jq --raw-output ".afp_password" $CONFIG_PATH)
AFP_UID=0
AFP_GID=0

if [ ! -z "${AFP_USER}" ]; then
    if [ ! -z "${AFP_UID}" ]; then
        cmd="$cmd -u ${AFP_UID}"
    fi
    adduser $cmd -H -D -g '' "${AFP_USER}"
    if [ ! -z "${AFP_PASSWORD}" ]; then
        echo "${AFP_USER}:${AFP_PASSWORD}" | chpasswd
    fi
fi

# create config
echo $'[Global]
log file = /dev/stdout
uam list = uams_guest.so uams_dhx2.so uams_dhx.so
hostname = homeassistant.local
[Share]
path = /share
valid users = %AFP_USER%
[Addons]
path = /addons
valid users = %AFP_USER%
[SSL]
path = /ssl
valid users = %AFP_USER%
[Configuration]
path = /config
valid users = %AFP_USER%
[Backup]
path = /backup
valid users = %AFP_USER%
[Time Machine]
path = /backup/timemachine
time machine = yes' >> /etc/afp.conf

# TODO: configure username/password
sed -i'' -e "s,%AFP_USER%,${AFP_USER:-},g" /etc/afp.conf

exec netatalk -F /etc/afp.conf -d
