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

# sed -i'' -e "s,%USER%,${AFP_USER:-},g" /etc/afp.conf

# create config
RUN echo $'[Global] \n\
log file = /dev/stdout \n\
uam list = uams_guest.so uams_dhx2.so uams_dhx.so \n\
[Share] \n\
path = /share \n\
valid users = $AFP_USER \n\
[Addons] \n\
path = /addons \n\
valid users = $AFP_USER \n\
[SSL] \n\
path = /ssl \n\
[Configuration] \n\
path = /config \n\
valid users = $AFP_USER \n\
[Backup] \n\
path = /backup \n\
valid users = $AFP_USER \n\
[Time Machine] \n\
path = /backup/timemachine \n\
time machine = yes' >> /etc/afp.conf

mkdir -p /var/run/dbus
rm -f /var/run/dbus/pid
dbus-daemon --system

rm -f /var/run/avahi-daemon/pid
sed -i '/rlimit-nproc/d' /etc/avahi/avahi-daemon.conf
avahi-daemon -D

# remove any previous lockfile that wasn't cleaned up
rm -f /var/run/lock/netatalk

exec netatalk -F /etc/afp.conf -d