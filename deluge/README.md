# Tkdrob's Hassio Add-ons: Deluge

## About

Deluge add-on based on the prebuilt docker image from linuxserver

Deluge is a BitTorrent client that utilizes a daemon/client model. It has various user interfaces available such as the GTK-UI, Web-UI and a Console-UI. It uses libtorrent at it's core to handle the BitTorrent protocol.

## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Hass.io add-on.

1. [Add my Hass.io add-ons repository][repository] to your Hass.io instance.
1. Install the add-on.
1. Click the `Save` button to store your configuration.
1. Start the  add-on.
1. Check the logs of the add-on to see if everything went well.
1. Carefully configure the add-on to your preferences, see the official documentation for that.


## Configuration

Access the webui at <your-ip>:8112, for more information check out https://deluge-torrent.org/

By default hassio folders backup, share and ssl are available within the addon.
You can use the share folder to access/store your media files.



[repository]: https://github.com/tkdrob/hassio-addons