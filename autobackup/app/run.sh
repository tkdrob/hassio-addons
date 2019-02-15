#!/bin/sh


CONFIG_PATH=/data/options.json
CRON_TASK=$(jq --raw-output ".schedule" $CONFIG_PATH)

# run app immediately if first run detected
if [ ! -f "/usr/src/app/firstrun" ]; then
    echo "First run detected, starting snapshot job"
    touch "/usr/src/app/firstrun"
    python /usr/src/app/main.py > /proc/1/fd/1 2>/proc/1/fd/2
fi

# apply cron schedule to crontab file
echo "Using cron schedule: $CRON_TASK"
rm /etc/crontabs/root
cronjob="$CRON_TASK python /usr/src/app/main.py > /proc/1/fd/1 2>/proc/1/fd/2"
echo -e "$cronjob\n\n" >> /etc/crontabs/root

# start crond with log level 8 in foreground, output to stderr
crond -f -d 8