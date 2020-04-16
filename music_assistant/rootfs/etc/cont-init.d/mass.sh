#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Community Add-on: MusicAssistant
# Configures MusicAssistant
# ==============================================================================


# Install latest version from GIT
if bashio::config.true 'use_nightly'; then
    bashio::log.green "Updating to latest GIT version..."
    curl -o /tmp/master.zip https://github.com/marcelveldt/musicassistant/archive/master.zip
    cd /tmp
    unzip master.zip
    cd /tmp/musicassistant-master
    python3 setup.py install
    rm -rf /tmp/musicassistant-master && \
    rm -f /tmp/master.zip
fi
