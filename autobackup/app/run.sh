#!/bin/sh


CONFIG_PATH=/data/options.json
CRON_TASK=$(jq --raw-output ".schedule" $CONFIG_PATH)
BACKUP_AT_START=$(jq --raw-output ".run_backup_at_startup" $CONFIG_PATH)
cronjob2=""

# run app immediately if first run detected
if [ "$BACKUP_AT_START" == "true" ]; then
    cronjob2="@reboot python /usr/src/app/main.py > /proc/1/fd/1 2>/proc/1/fd/2"
fi

# apply cron schedule to crontab file
echo "Using cron schedule: $CRON_TASK"
rm /etc/crontabs/root
cronjob="$CRON_TASK python /usr/src/app/main.py > /proc/1/fd/1 2>/proc/1/fd/2"
echo -e "$cronjob\n$cronjob2\n" >> /etc/crontabs/root

# start crond with log level 8 in foreground, output to stderr
crond -f -d 8