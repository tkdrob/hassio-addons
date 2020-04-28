# Tkdrob's Hassio Add-ons: Openvpn Connect

## About

Openvpn Connect add-on based on the prebuilt docker image from dperson

This is an OpenVPN client docker container. It makes routing containers' traffic through OpenVPN easy.

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

There is no ui for this container. The port configurations are for the services that you want to use behind the vpn. The preconfigured ports can be changed by editing the config.json file for this addon. For more information, check out https://github.com/dperson/openvpn-client/

By default hassio folders backup, share and ssl are available within the addon.
You can use the share folder to access/store your media files.



[repository]: https://github.com/tkdrob/hassio-addons