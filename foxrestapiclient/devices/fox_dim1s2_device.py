"""F&F Fox DIM1S2 device implementation."""

from .fox_base_device import DeviceData
from .fox_dimmable_device import FoxDimmableDevice

class FoxDIM1S2Device(FoxDimmableDevice):
    """DIM1S2 device one channel dimmer 230V."""

    def __init__(self, device_data: DeviceData):
        """Initalize object."""
        super().__init__(device_data)
        self.brightness = 0
        self.state = False

    def is_on(self, channel: int = None):
        """Return device state idicates to turn on or off."""
        return self.state

    async def async_fetch_update(self):
        """Fetch all available data from device."""
        self.state = await self.async_fetch_channel_state()
        channel_brightness = await self.async_fetch_channel_brightness()
        if isinstance(channel_brightness, list):
            self.brightness = channel_brightness[0]
        else:
            self.brightness = 0