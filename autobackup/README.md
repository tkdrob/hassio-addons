# Marcelveldt's Hassio Add-ons: Auto backup

## About

Automatically create snapshots of your hassio installation and optionally upload them to the cloud (currently only Google Drive).
No need to create tasks yourself in HomeAssistant automations, this add-on will take of the scheduling, backupping and even uploading to the cloud.
By default the snapshot will contain your homeassistant and hassio configuration, the ssl folder and the local addons folder.
Installed addons and your share folder (even on a subfolder level) can be optionally included in the snapshot.

## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Hass.io add-on.

1. [Add my Hass.io add-ons repository][repository] to your Hass.io instance.
1. Install the "Auto Backup" add-on.
1. Carefully configure the add-on to your preference with the options (see below).
1. Click the `Save` button to store your configuration.
1. Start the "Auto Backup" add-on.
1. Check the logs of the add-on to see if everything went well.
1. At the first start, a first snapshot is created immediately, once done it will follow the schedule
1. If you enabled upload to Google Drive, the log will tell you to authenticate, use the "Open Web UI" button for that.
1. Ready to go!



## Configuration

**Note**: _Remember to restart the add-on when the configuration is changed._

Example add-on configuration:

```json
{
  "log_level": "INFO",
  "log_file": "/backup/autobackup.log",
  "schedule": "0 4 * * *",
  "backup_addons": {
    "enabled": true,
    "whitelist": [],
    "blacklist": []
  },
  "backup_share": {
    "enabled": true,
    "subfolders": [
      "tools",
      "music"
    ]
  },
  "auto_purge": 3,
  "google_drive": {
    "enabled": true,
    "auto_purge": 2,
    "backup_folder": "hassio_backups"
  }
}
```

**Note**: _This is just an example, don't copy and paste it! Create your own!_

### Option: `log_level`

The `log_level` option controls the level of log output by the addon and can
be changed to be more or less verbose, which might be useful when you are
dealing with an unknown issue. Possible values are:

- `DEBUG`: Shows detailed debug information.
- `INFO`: Normal (usually) interesting events. It's the default choice.
- `WARNING`: Exceptional occurrences that are not errors.
- `ERROR`: Something went terribly wrong. Add-on becomes unusable.

**Note**: _The loglevel is only applied to the logfile, not the console output._

### Option: `log_file`

Full path to the logfile. Root folder can be either /backup or /share. The addon does not have access to other hassio folders.

### Option: `schedule`

Schedule when the backup task should run. By default it's set to every night at 04:00.
You can use CRON syntax for this. http://www.nncron.ru/help/EN/working/cron-format.htm

### Option: `backup_addons`

This setting allows you to include installed addons (and their configuration) into the snapshot.
`enabled`: include installed addons in the snapshot.
`whitelist`: (optional) only include addons in this list the snapshot.
`blacklist`: (optional) include all addons except in items in this list the snapshot.

If you do not specify whitelist and blacklist items, all addons will be included in the snapshot.
You can use either use the full name for an addon or the short name (which you will have to figure out yourself)

### Option: `backup_share`

This setting allows you to include the share folder into the snapshot.
`enabled`: include share folder in the snapshot.
`subfolders`: (optional) only include these files/subfolders from /share in the snapshot.

**Note**: _In many cases the share folder is used to store mediafiles etc. and when the subfolders option is ommitted, the snapshot can grow large!._

### Option: `auto_purge`

Automatically purge old snapshot from hassio.
The latest X snapshots will be kept. Set to 0 to disable the auto purging.

### Option: `google_drive`

This setting allows you to enable auto upload of your snapshots to Google Drive.
`enabled`: enable auto uploading of snapshots to Google Drive.
`auto_purge`: Automatically purge old snapshot from Google Drive. The latest X snapshots will be kept. Set to 0 to disable the auto purging.
`backup_folder`: The name of the folder on your Google Drive where to store snapshots (will be created if not exists).

If you enable the Google Drive upload, the add-on will ask you to authorize the app once when the first/next backup task is run.
Check the log for details.


[repository]: https://github.com/marcelveldt/hassio-addons-repo