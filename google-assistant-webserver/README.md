# Marcelveldt's Hassio Add-ons: Google Assistant Webserver

## About

Webservice for the Google Assistant SDK - mofified version of the original by @AndBobsYourUncle with customizable broadcast command
For my own personal use but maybe some other non-English hassio users can benefit from this too.


## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Hass.io add-on.

1. [Add my Hass.io add-ons repository][repository] to your Hass.io instance.
1. Install the "Google Assistant Webserver" add-on.
1. Start the "Google Assistant Webserver" add-on.
1. Check the logs of the add-on to see if everything went well.
1. At the first start, you will need to authenticate with Google, use the "Open Web UI" button for that.
1. Ready to go!



## Configuration

**Note**: _Remember to restart the add-on when the configuration is changed._

Example add-on configuration:

```json
{
  "broadcast_cmd": "vertel iedereen"
}
```

**Note**: _This is just an example, don't copy and paste it! Create your own!_

### Option: `broadcast_cmd`

The `broadcast_cmd` option allow you to specify a custom phrase for the broadcast command.
By default (in English) it is "broadcast" but in other languages this will be something else, like "vertel iedereen" (in Dutch).


[repository]: https://github.com/marcelveldt/hassio-addons-repo