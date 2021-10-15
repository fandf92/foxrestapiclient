"""F&F Fox STR1S2 device implementation."""

from __future__ import annotations
import logging
from .fox_base_device import DeviceData, FoxBaseDevice
from foxrestapiclient.connection.rest_api_client import RestApiClient
from foxrestapiclient.connection.rest_api_responses import RestApiBaseResponse
from foxrestapiclient.connection.const import (
    API_RESPONSE_STATUS_FAIL,
    API_RESPONSE_STATUS_OK,
)
from .const import (
    API_STR1S2_GET_OPEN_LEVEL,
    API_STR1S2_SET_OPEN_LEVEL,
    API_STR1S2_GET_TILT_LEVEL,
    API_STR1S2_SET_TILT_LEVEL
)
import json

class FoxSTR1S2Device(FoxBaseDevice):
    """STR1S2 rollershutter device."""

    def __init__(self, device_data: DeviceData):
        """Initalize object."""
        super().__init__(device_data.name, device_data.host, device_data.api_key,
                        device_data.mac_addr, device_data.type)
        #State reprsents cover open or close
        self._state = False
        self.__device_api_client = self.DeviceRestApiImplementer(super())
        self._cover_position = 0
        self._tilt_position = 0

    class CoverOpenLevel(RestApiBaseResponse):
        """Cover open level data holder."""

        def __init__(self, level: str = None, status: str = API_RESPONSE_STATUS_FAIL) -> None:
            """Initialize object."""
            super().__init__(status)
            self.level = 0
            try:
                self.level = int(level)
            except:
                self.level = 0

    class DeviceRestApiImplementer(RestApiClient):
        """Specific RestAPI methods definition used by device."""

        def __init__(self, restApiClient: RestApiClient) -> None:
            """Initalize object."""
            self._restApiClient = restApiClient

        async def async_fetch_level(self, method: str) -> FoxSTR1S2Device.CoverOpenLevel:
            """Get open level api method."""
            device_response = await self._restApiClient.async_make_api_call_get(method)
            if device_response is None:
                return FoxSTR1S2Device.CoverOpenLevel(status=API_RESPONSE_STATUS_FAIL)
            return FoxSTR1S2Device.CoverOpenLevel(**json.loads(device_response))

        async def async_get_open_level(self) -> FoxSTR1S2Device.CoverOpenLevel:
            """Get cover open level."""
            return await self.async_fetch_level(API_STR1S2_GET_OPEN_LEVEL)

        async def async_get_tilt_level(self) -> FoxSTR1S2Device.CoverOpenLevel:
            """Get tilt level."""
            return await self.async_fetch_level(API_STR1S2_GET_TILT_LEVEL)

        async def update_open_level(self, params, method)  -> RestApiBaseResponse:
            """Set open level api method."""
            device_response = await self._restApiClient.async_make_api_call_get(method, params)
            if device_response is None:
                return RestApiBaseResponse(status=API_RESPONSE_STATUS_FAIL)
            return RestApiBaseResponse(**json.loads(device_response))

        async def async_set_open_level(self, params) -> RestApiBaseResponse:
            """Set open cover level."""
            return await self.update_open_level(params, API_STR1S2_SET_OPEN_LEVEL)

        async def async_set_tilt_open_level(self, params) -> RestApiBaseResponse:
            """Set tilt open level."""
            return await self.update_open_level(params, API_STR1S2_SET_TILT_LEVEL)

    def is_on(self, channel: int = None):
        """Return device state."""
        logging.warning("This device does not support is on funcionality.")
        return None

    def is_cover_opened(self):
        """Get is cover open.

        Open means position is greater than 0.
        """
        return True if self._cover_position > 0 else False

    def is_cover_closed(self):
        """Get is cover closed."""
        return True if self._cover_position == 0 else False

    def get_cover_position(self):
        """Get cover postion."""
        return self._cover_position

    def get_tilt_position(self):
        """Get tilt position."""
        return self._tilt_position

    async def __async_fetch_open_level(self, callback = None, is_cover = True):
        """Fetch cover open level."""
        if callback is None:
            return
        cover_open = await callback()
        if cover_open.status != API_RESPONSE_STATUS_OK:
            self._state = False
            return
        if is_cover:
            self._cover_position = cover_open.level
        else:
            self._tilt_position = cover_open.level

    async def async_fetch_cover_open_level(self):
        """Fetch cover open level."""
        await self.__async_fetch_open_level(self.__device_api_client.async_get_open_level)

    async def async_fetch_tilt_open_level(self):
        """Fetch tilt open level."""
        await self.__async_fetch_open_level(self.__device_api_client.async_get_tilt_level, False)

    async def __async_cover_set_level(self, level = 0, is_cover = True):
        """Set cover level.

        Keyword arguments:
        level -- cover position must be in range <0,100>
        callback -- function to call
        """
        if level < 0 or level > 100:
            logging.warning("Level passed to __async_cover_set_level is out of range. Supported <0,100>")
            return
        params = {
            "level": level
        }
        if is_cover == True:
            device_response = await self.__device_api_client.async_set_open_level(params)
        else:
            device_response = await self.__device_api_client.async_set_tilt_open_level(params)
        if device_response.status != API_RESPONSE_STATUS_OK:
            self._state = False
            return
        self._state = True

    async def async_open_cover(self):
        """Open cover."""
        await self.__async_cover_set_level(100)

    async def async_close_cover(self):
        """Close cover."""
        await self.__async_cover_set_level(0)

    async def async_set_cover_position(self, position):
        """Set cover position."""
        await self.__async_cover_set_level(position)

    async def async_set_tilt_positon(self, position):
        """Set tilt position."""
        await self.__async_cover_set_level(position, False)

    async def async_set_device_state(self, is_on, channel = None):
        """Overriden method from base device."""
        logging.warning("This device does not support set_device_state funcionality.")

    async def async_fetch_channel_state(self, channel: int = None) -> bool | list:
        """Overriden method from base device."""
        logging.warning("This device does not support fetch_channel_state funcionality.")

    async def async_update_channel_state(self, state: bool, channel: int = None) -> bool:
        """Overriden method from base device."""
        logging.warning("This device does not support update_channel_state funcionality.")

    async def async_fetch_update(self):
        """Fetch all available data from device."""
        await self.async_fetch_cover_open_level()
        await self.async_fetch_tilt_open_level()