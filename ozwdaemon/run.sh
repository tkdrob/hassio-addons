#!/bin/bash
set -e

CONFIG_PATH=/data/options.json

function file_exists () {
    # check if a path (partly) exists
    for f in $1; do
        [ -e "$f" ] && return 1 || return 0
        break
    done
}

# Migrate existing/previous data from hass config folder
if [[ $(file_exists "/data/ozwcache_*"; echo $?) -eq 0 ]]; then
    if [[ $(file_exists "/config/ozwcache_*"; echo $?) -eq 1 ]]; then
        echo "[INFO] Migrating existing ozw_cache*.xml from /config"
        cp /config/ozwcache_* /data
    fi
fi
if [ ! -f "/data/options.xml" ]; then
    if [ -f "/config/options.xml" ]; then
        echo "[INFO] Migrating existing options.xml from /config"
        cp /config/options.xml /data
    fi
fi

# TODO: Auto detect path to Z-wave device
ZWAVE_DEVICE=$(jq --raw-output '.zwave_device' $CONFIG_PATH)
OZW_INSTANCE=$(jq --raw-output '.ozw_instance' $CONFIG_PATH)

# TODO: Find a better way to supply the Network key
export OZW_NETWORK_KEY=$(jq --raw-output '.zwave_network_key' $CONFIG_PATH)

MQTT_CONFIG=

# Use Hass.io mqtt services
if MQTT_CONFIG="$(curl -s -f -H "X-Hassio-Key: ${HASSIO_TOKEN}" http://hassio/services/mqtt)"; then
    HOST="$(echo "${MQTT_CONFIG}" | jq --raw-output '.data.host')"
    PORT="$(echo "${MQTT_CONFIG}" | jq --raw-output '.data.port')"
    USER="$(echo "${MQTT_CONFIG}" | jq --raw-output '.data.username')"
    PASSWORD="$(echo "${MQTT_CONFIG}" | jq --raw-output '.data.password')"

    echo "[INFO] Setup Hass.io mqtt service to ${HOST}"

else
    echo "[ERROR] No Hass.io mqtt service found!"
    exit 1
fi

export OZW_INSTANCE=$OZW_INSTANCE
export ZWAVE_DEVICE=$ZWAVE_DEVICE
export MQTT_HOST=$HOST
export MQTT_PORT=$PORT
export MQTT_USER=$USER
export MQTT_PASSWORD=$PASSWORD
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf