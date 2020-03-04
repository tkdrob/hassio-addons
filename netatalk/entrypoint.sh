#!/bin/bash

if [ ! -z "${AFP_USER}" ]; then
    if [ ! -z "${AFP_UID}" ]; then
        cmd="$cmd --uid ${AFP_UID}"
    fi
    if [ ! -z "${AFP_GID}" ]; then
        cmd="$cmd --gid ${AFP_GID}"
        groupadd --gid ${AFP_GID} ${AFP_USER}
    fi
    adduser $cmd --no-create-home --disabled-password --gecos '' "${AFP_USER}"
    if [ ! -z "${AFP_PASSWORD}" ]; then
        echo "${AFP_USER}:${AFP_PASSWORD}" | chpasswd
    fi
fi

# create config
echo $'[Global]
log file = /dev/stdout
uam list = uams_guest.so uams_dhx2.so uams_dhx.so
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
# configure listen ip
# DOCKER_HOST=`/sbin/ip route|awk '/default/ { print $3 }'`
# sed -i'' -e "s,%HOST_IP%,${DOCKER_HOST:-},g" /etc/afp.conf

mkdir -p /var/run/dbus
rm -f /var/run/dbus/pid
dbus-daemon --system

rm -f /var/run/avahi-daemon/pid
sed -i '/rlimit-nproc/d' /etc/avahi/avahi-daemon.conf
sed -i'' -e "s,#enable-dbus,enable-dbus,g" /etc/avahi/avahi-daemon.conf
avahi-daemon -D

# remove any previous lockfile that wasn't cleaned up
rm -f /var/run/lock/netatalk

exec netatalk -F /etc/afp.conf -d
