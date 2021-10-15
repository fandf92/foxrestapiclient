"""F&F Fox base device implementation."""
from __future__ import annotations
import abc

from aiohttp.client_exceptions import ClientConnectionError
from foxrestapiclient.connection.rest_api_client import RestApiClient
from foxrestapiclient.connection.rest_api_responses import RestApiDeviceInfoResponse
from .const import (
    API_RESPONSE_STATUS_FAIL,
    API_RESPONSE_STATUS_INVALID,
    DEVICES,
    DEVICE_ON,
    DEVICE_OFF,
    DEVICE_PLATFORM,
    MANUFACTURER_NAME
)

class DeviceData:
    """DeviceData holder. Used for simple object creation."""

    def __init__(self, name: str, host: str, api_key: str, mac_addr: str, type: int, channels: list = None):
        """Init all required values."""
        self.name = name
        self.host = host
        self.api_key = api_key
        self.mac_addr = mac_addr
        self.type = type
        self.channels = channels

class UnsupportedDevice(Exception):
    """Custom exception for unsupported device."""

    pass

class FoxBaseDevice(RestApiClient):
    """F&F Fox base device class."""

    __metaclass__ = abc.ABCMeta
    def __init__(self, name: str, host: str, api_key: str, mac_addr: str,
                type: int):
        """Construct object with data passed. Warning! can be exception raised."""
        super().__init__(host, api_key)
        self.__init_device_platform(type)
        self.type = type
        self.name = name
        self.mac_addr = mac_addr
        self.device_info_data: RestApiDeviceInfoResponse = None
        self.is_available = False

    def __init_device_platform(self, type: int):
        """Initialize device platform.

        Keyword arguments:
        type -- device type, determine platfom by this value.

        Warning!
        If type not exsist in DEVICE_PLATFORM exception UnsupportedDevice will be raised.
        """
        try:
            self.device_platform = DEVICE_PLATFORM[type]
            self.register_response_error_hook(self.__track_available)
        except:
            raise UnsupportedDevice("Not supported device. Check type param.")

    def equals(self, foxBaseDevice: FoxBaseDevice) -> bool:
        """Compare object and return that are equal.

        Comparation works on unique identifier.

        Keyword arguments:
        foxBaseDevice -- device base object to compare to

        Return:
        true if devices are equal.
        """
        if foxBaseDevice is None:
            return False
        if self.mac_addr == foxBaseDevice.mac_addr:
            return True
        return False

    def __track_available(self, error):
        """Track device availability."""
        if isinstance(error, ClientConnectionError):
            self.is_available = False
        if error is None:
            self.is_available = True

    def get_channel_name(self, channel: int) -> str:
        """Return channel name or name."""
        if channel < 1 and channel > 2:
            return self.name
        if len(self.device_info_data.device_channels_name) > 0:
            return self.device_info_data.device_channels_name[channel-1]
        return self.name

    def get_device_info(self) -> str:
        """Get device info JSON string.

        This method is similar to HomeAssistant get_device_info()
        Can be easy adapted to HA system.

        Return:
        JSON string contains device info.
        """
        name = self.name
        sw_version = "0.0.0"
        if self.device_info_data is not None:
            name = self.device_info_data.device_friendly_name
            sw_version = self.device_info_data.firmware,

        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (self.device_platform, self.mac_addr)
            },
            "name": name,
            "manufacturer": MANUFACTURER_NAME,
            "model": DEVICES[self.type],
            "sw_version": sw_version
        }

    async def async_set_device_state(self, is_on, channel = None):
        """Set device state.

        Set state on or off on F&F Fox device.

        Keyword arguments:
        is_on -- determine to set device on, if true device will be turned on otherwise turned off.
        channel -- optional, set state on specified channel.
        """
        device_state = await self.async_api_set_device_state(is_on, channel)
        if (device_state.status == API_RESPONSE_STATUS_FAIL
            or device_state.status == API_RESPONSE_STATUS_INVALID):
            self._state = False
        elif device_state == DEVICE_ON:
            self._state = True
        else:
            self._state = False

    async def async_fetch_channel_state(self, channel: int = None) -> bool | list:
        """Fetch device state.

        Fetch F&F Fox device state by given channel. If None provided
        device get_state generic method will be used. This method can
        return list bool values or single bool value.

        Keyword arguments:
        channel -- optional, fetch state by given channel

        Return:
        list[bool] - if no channel provided and device has more than one channel
                     index 0 idicates to channel 1, index 1 to channel 2
        bool - device has only one channel, true or false.
        """
        device_response = await self.async_api_get_device_state(channel)
        if (device_response.status == API_RESPONSE_STATUS_FAIL or
                device_response.status == API_RESPONSE_STATUS_INVALID):
            self.is_available = False
            return False
        self.is_available = True
        if device_response.state == DEVICE_ON:
            return True
        elif device_response.state == DEVICE_OFF:
            return False
        values = []
        if device_response.channel_1_state == DEVICE_ON:
             values.append(True)
        else:
            values.append(False)
        if device_response.channel_2_state == DEVICE_ON:
            values.append(True)
        else:
            values.append(False)
        return values if values != [] else [False, False]

    async def async_update_channel_state(self, state: bool, channel: int = None) -> bool:
        """Update device state.

        Update F&F Fox device state. Turn it on or off.

        Keyword arguments:
        state -- value to set on device, true or false, where true means turn on.
        channel -- optional, set state by given channel.

        Return:
        true or false depends on device response.
        """
        device_response = await self.async_api_set_device_state(state, channel)
        if (device_response.status == API_RESPONSE_STATUS_FAIL or
                device_response.status == API_RESPONSE_STATUS_INVALID):
            return False
        elif device_response.status == DEVICE_ON:
            return True
        else:
            return False

    async def async_fetch_device_info(self):
        """Fetch device info.

        Fetch F&F Fox device info. Name, firmware version etc. see RestApiDeviceInfoResponse.
        Warning! this method will override device name provided in constructor. Device name defined
        in Fox mobile application has priority.
        """
        device_response: RestApiDeviceInfoResponse = await self.async_api_get_device_info()
        if (device_response.status == API_RESPONSE_STATUS_FAIL or
                device_response.status == API_RESPONSE_STATUS_INVALID):
            return
        self.device_info_data = device_response
        #Overwrite device name from user app config
        if device_response.device_name is not None:
            self.name = device_response.device_name

    async def async_fetch_device_available_data(self):
        """Fetch all available data from device."""
        await self.async_fetch_device_info()
        await self.async_fetch_update()

    @abc.abstractmethod
    def is_on(self, channel: int = None):
        """Return device state to determine that is on or off."""

    @abc.abstractmethod
    async def async_fetch_update(self):
        """Abstract method - fetch data from device."""