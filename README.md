# RestAPI Client for F&F Fox devices

This package contains simple RestAPI client written in Python for [F&F Filipowski Sp. j.](https://www.fif.com.pl) Fox devices such as single switch & energy (R1S1), double switch (R2S2), led (LED2S2), dimmer (DIM1S2), color module (RGBW), roller shutter (STR1S2).

### Requirements

To obtain communication with device you should firstly configure it via F&F Fox mobile application available on [Android](https://play.google.com/store/apps/details?id=pl.com.fif.fox) and [IOS](https://apps.apple.com/pl/app/fox/id1580578557?l=pl) (instructions included in app). Next grant access to remote control and enable RestAPI server with one of the following mode

- **Static** RestAPI client auth key

- **Dynamic** RestAPI client auth key
- No auth key (**default 000 should be used**)

**Attention**
All F&F Fox devices supports now only HTTP GET request method. In near future **mqtt client** will be available.

### Features

- Async API device communication
- Turn on/off device
- Change brightness (DIM1S2, LED2S2, RGBW)
- Change color in HSV mode (RGBW)
- Open/Close gate (STR1S2)
- Change tilt position (STR1S2)
- Get device information (such as manufacturer, firmaware version etc.)

### Example - Toggle state of channel

To run this example first clone and install our client library.

```bash
python3 -m venv venv
source venv/bin/activate
git clone https://github.com/fandf92/foxrestapiclient.git
cd foxrestapiclient/ && python setup.py install
```

The following example illustrates how to configure and use F&F Fox double switch module via our client.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from foxrestapiclient.devices.fox_r2s2_device import DeviceData, FoxR2S2Device
from foxrestapiclient.devices.const import DEVICE_TYPE_R2S2


async def main():
    # Name: name of device
    NAME = None
    # Host: device IP address (e.g 192.168.0.100)
    HOST = '_device_IP_address_'
    # API_KEY: auth api key, get it from F&F Fox mobile app
    API_KEY = '0000' # The API key is set to 0000 when the type REST API is set to "key not required"
    # UNIQUE_ID: unique id for device
    UNIQUE_ID = None
    # TYPE: device type (see wiki page)
    TYPE = DEVICE_TYPE_R2S2
    # CHANNELS: optional channel array. Eg. [1, 2]
    CHANNELS = None
    # Channel ID which we want to toggle
    CHANNEL_ID_TO_TOGGLE = 2

    doubleSwitch = FoxR2S2Device(DeviceData(
        name=NAME, host=HOST, api_key=API_KEY, mac_addr=UNIQUE_ID, dev_type=TYPE, channels=CHANNELS))

    # Fetching all available info of device: general device data and product specify values
    await doubleSwitch.async_fetch_device_available_data()

    # Toggle state of channel
    channelStateToSet = not doubleSwitch.channel_two_state
    apiResult = await doubleSwitch.async_update_channel_state(channelStateToSet, CHANNEL_ID_TO_TOGGLE)
    if apiResult:
        print(
            f'> Channel {CHANNEL_ID_TO_TOGGLE} toggled to {channelStateToSet} <')

    friendlyName = doubleSwitch.device_info_data.device_friendly_name
    channelsNames = doubleSwitch.device_info_data.device_channels_name

    # Print friendly name and channels names
    print(f'Device firendly name "{friendlyName}"')
    print(f'It\'s channels names {channelsNames}')

if __name__ == '__main__':
    asyncio.run(main())
    pass

```

More information about how to control device via API methods you can find on wiki [page](https://github.com/fandf92/foxrestapiclient/wiki).
