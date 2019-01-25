#!/bin/bash
set -e

# MOFIFY DATA PATH
sed -i "s|config|data|g" /var/run/s6/services/sonarr/run
./init
