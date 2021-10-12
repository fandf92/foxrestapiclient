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

### Example

The following example illustrate how to configure F&F Fox double switch module

```python
doubleSwitch = FoxR2S2Device(
	DeviceData(NAME, HOST, API_KEY, UNIQUE_ID, TYPE, CHANNELS))
```
- Name: name of device
- Host: device IP address (e.g 192.168.0.100)
- API_KEY: auth api key, get it from F&F Fox mobile app
- UNIQUE_ID: unique id for device
- TYPE: device type (see wiki page)
- CHANNELS: optional channel array

**Turning on device:**
```python
await doubleSwitch.async_set_device_state(True)
```

More information about how to control device via API methods you can find on wiki [page](https://github.com/fandf92/foxrestapiclient/wiki).