# Tkdrob's Hassio Add-ons: Sonarr

## About

Jackett add-on based on the prebuilt docker image from linuxserver

Jackett provides API Support for your favorite torrent trackers. Jackett works as a proxy server: it translates queries from apps (Sonarr, Radarr, SickRage, CouchPotato, Mylar, Lidarr, DuckieTV, qBittorrent, Nefarious etc.) into tracker-site-specific http queries, parses the html response, then sends results back to the requesting software. This allows for getting recent uploads (like RSS) and performing searches. Jackett is a single repository of maintained indexer scraping & translation logic - removing the burden from other apps.

## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Hass.io add-on.

1. [Add my Hass.io add-ons repository][repository] to your Hass.io instance.
1. Install the add-on.
1. Click the `Save` button to store your configuration.
1. Start the  add-on.
1. Check the logs of the add-on to see if everything went well.
1. Carefully configure the add-on to your preferences, see the official documentation for for that.


## Configuration

Access the webui at <your-ip>:9117, for more information check out https://github.com/Jackett/Jackett/

By default hassio folders backup, share and ssl are available within the addon.
You can use the share folder to access/store your media files.



[repository]: https://github.com/tkdrob/hassio-addons