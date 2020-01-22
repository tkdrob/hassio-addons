## Home Assistant Z-Wave over MQTT Integration (Pre-Release)


This add-on is a wrapper for the docker image provided here: https://github.com/OpenZWave/qt-openzwave
OpenZWave's qt-openzwave allows you to control a Z-Wave network over MQTT. It is currently available as a custom component through HACS and will be submitted as an official Home Assistant component once it has matured a bit.

For more information, see the GitHub repository for the hass component:
https://github.com/cgarwood/homeassistant-zwave_mqtt



## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Hass.io add-on.

1. [Add my Hass.io add-ons repository][repository] to your Hass.io instance.
1. Install this add-on.
1. Click the `Save` button to store your configuration.
1. Start the add-on.
1. Check the logs of the add-on to see if everything went well.
1. Carefully configure the add-on to your preferences, see the official documentation for for that.


## Configuration

Some manual configuration is still needed at the moment.
It is required that you have MQTT setup in HomeAssistant! Hassio includes a Mosquitto MQTT broker addon.

### Option: `zwave_device`

Path to your Z-wave stick/device. Default to /dev/ttyACM0

### Option: `zwave_network_key`

For secure communication it is required that you provide a secure network key.
Only required if you actually want to include secure devices to your Z-wave mesh,

### Option: `ozw_instance`

Advanced usage only. If you want to connect multiple OZW instances to HomeAssistant.
Defaults to 1.


[repository]: https://github.com/marcelveldt/hassio-addons-repo
