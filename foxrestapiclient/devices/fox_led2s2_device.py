"""F&F Fox LED2S2 device implementation."""

import logging
from .fox_base_device import DeviceData
from .fox_dimmable_device import FoxDimmableDevice

class FoxLED2S2Device(FoxDimmableDevice):
    """LED2S2 Device implementation."""

    def __init__(self, device_data: DeviceData):
        """Initialze object."""
        super().__init__(device_data)
        #This device has two channels
        self.channels = [1, 2]
        self.channel_one_state = False
        self.channel_two_state = False
        #Store brighntess value for each channel
        self.channel_one_brightness = 0
        self.channel_two_brightness = 0

    def is_on(self, channel: int = None) -> bool:
        """Return device state to determine that is on or off.

        Keyword arguments:
        channel -- channel number to check that is on or off. Must be in ranfe <1,2>
        """
        if channel < 0 or channel > 2:
            logging.warning("Channel provided to is_on() is out of range.")
            return False
        return self.channel_one_state if channel == 1 else self.channel_two_state

    async def async_fetch_channel_one_state(self) -> bool:
        """Fetch device state on channel one."""
        self.channel_one_state = await self.async_fetch_channel_state(self.channels[0])
        return self.channel_one_state

    async def async_fetch_channel_two_state(self) -> bool:
        """Fetch device state on channel two."""
        self.channel_one_state = await self.async_fetch_channel_state(self.channels[1])
        return self.channel_two_state

    async def async_update_channel_one_state(self, state: bool):
        """Update device channel one state by given value."""
        self.channel_one_state = await self.async_update_channel_state(state, self.channels[0])

    async def async_update_channel_two_state(self, state: bool):
        """Update device channel one state by given value."""
        self.channel_two_state = await self.async_update_channel_state(state, self.channels[1])

    async def async_fetch_channel_one_brightness(self) -> int:
        """Fetch channel one brightness value."""
        channel_brightness = await self.async_fetch_channel_brightness(self.channels[0])
        if isinstance(channel_brightness, list):
            self.channel_one_brightness = channel_brightness[0]
        else:
            self.channel_one_brightness = 0
        return self.channel_one_brightness

    async def async_fetch_channel_two_brightness(self) -> int:
        """Fetch channel two brightness value."""
        channel_brightness = await self.async_fetch_channel_brightness(self.channels[1])
        if isinstance(channel_brightness, list):
            self.channel_two_brightness = channel_brightness[0]
        else:
            self.channel_two_brightness = 0
        return self.channel_two_brightness

    async def async_update_channel_one_brightness(self):
        """Update channel one brightness."""
        self.channel_one_brightness = await self.async_update_channel_brightness(self.channels[0])

    async def async_update_channel_two_brightness(self):
        """Update channel two brightness."""
        self.channel_two_brightness = await self.async_update_channel_brightness(self.channels[1])

    def __reset_channels_state(self):
        """Reset channels state."""
        self.channel_one_state = False
        self.channel_two_state = False

    def __reset_channels_brighntess(self):
        """Reset channels brightness."""
        self.channel_one_brightness = 0
        self.channel_two_brightness = 0

    async def async_fetch_update(self):
        """Fetch all available data from device."""
        states = await self.async_fetch_channel_state()
        if not isinstance(states, list):
            self.__reset_channels_state()
        else:
            self.channel_one_state, self.channel_two_state = states
        brigntess = await self.async_fetch_channel_brightness()
        if not isinstance(brigntess, list):
            self.__reset_channels_brighntess()
        elif isinstance(brigntess, list) and len(brigntess) < 2:
            self.__reset_channels_brighntess()
        else:
            self.channel_one_brightness, self.channel_two_brightness = brigntess