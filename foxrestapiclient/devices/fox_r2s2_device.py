"""F&F Fox R2S2 device implementation."""

import logging
from .fox_base_device import DeviceData, FoxBaseDevice

class FoxR2S2Device(FoxBaseDevice):
    """F&F Fox R2S2 device implementation. Two relays and two switches."""

    def __init__(self, device_data: DeviceData):
        """Initalize object."""
        super().__init__(device_data.name, device_data.host, device_data.api_key,
                        device_data.mac_addr, device_data.type)
        #This device has two channels
        self.channels = [1, 2]
        self.channel_one_state = False
        self.channel_two_state = False

    def is_on(self, channel: int) -> bool:
        """Return device is on status.

        Return F&F Fox R2S2 device status. Check if it is on by given channel.

        Keyword arguments:
        channel -- required parameter to obtain status. Can be 1 or 2.
        Return:
        channel state, on or off.
        """
        if channel < 0 or channel > 2:
            logging.warning("Passed channel in is_on() has wrong value. Only 1 or 2 are accepted.")
            return False
        return self.channel_one_state if channel == 1 else self.channel_two_state

    def __set_channels_to_off(self):
        """Private method to reseting channels state."""
        self.channel_one_state = False
        self.channel_two_state = False

    async def async_fetch_update(self):
        """Abstract method implementation. Fetch all required data from device."""
        states = await self.async_fetch_channel_state()
        if states is not None and isinstance(states, list):
            self.channel_one_state, self.channel_two_state = await self.async_fetch_channel_state()
        else:
            self.__set_channels_to_off()