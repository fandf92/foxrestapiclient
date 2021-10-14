"""F&F Fox RGBW device implementation."""

from __future__ import annotations
from .fox_base_device import DeviceData, FoxBaseDevice
from foxrestapiclient.connection.rest_api_client import RestApiClient
from foxrestapiclient.connection.rest_api_responses import RestApiBaseResponse
from foxrestapiclient.connection.const import (
    API_RESPONSE_STATUS_FAIL,
    API_RESPONSE_STATUS_OK,
)
from .const import (
    API_RGBW_SET_COLOR_HSV,
    API_RGBW_GET_COLOR_HSV
)
import json

class FoxRGBWDevice(FoxBaseDevice):
    """Fox RGBW device."""

    def __init__(self, device_data: DeviceData):
        """Initalize object."""
        super().__init__(device_data.name, device_data.host, device_data.api_key,
                        device_data.mac_addr, device_data.type)
        self.hsv_color = [0, 0, 0]
        self.__device_api_client = self.DeviceRestApiImplementer(super())
        self._state = False

    class HSVColorData(RestApiBaseResponse):
        """HSV color data holder."""

        def __init__(self, h: str = None, s: str = None, v: str = None,
                    status: str = API_RESPONSE_STATUS_FAIL) -> None:
            """Initalize object."""
            super().__init__(status)
            self.hue = self.try_parse_to_int(h)
            self.saturation = self.try_parse_to_int(s)
            #Brightness value
            self.value = int((self.try_parse_to_int(v) * 255) / 100)

        def try_parse_to_int(self, value):
            """Try parse given value to int.

            Keyword arguments:
            value -- value to parse.
            Return: parsed value to int or 0 if parsing went wrong.
            """
            try:
                return int(value)
            except:
                return 0

    class DeviceRestApiImplementer:
        """Specific RestAPI methods definition used by device."""

        def __init__(self, restApiClient: RestApiClient) -> None:
            """Initialize object."""
            self._restApiClient = restApiClient

        async def async_get_hsv_color(self) -> FoxRGBWDevice.HSVColorData:
            """Get HSV values by given channel."""
            device_response = await self._restApiClient.async_make_api_call_get(API_RGBW_GET_COLOR_HSV)
            if device_response is None:
                return FoxRGBWDevice.HSVColorData(status=API_RESPONSE_STATUS_FAIL)
            return FoxRGBWDevice.HSVColorData(**json.loads(device_response))

        async def async_set_hsv_color(self, params = None) -> RestApiBaseResponse:
            """Set HSV values by given channel."""
            device_response = await self._restApiClient.async_make_api_call_get(API_RGBW_SET_COLOR_HSV, params)
            if device_response is None:
                return RestApiBaseResponse(status=API_RESPONSE_STATUS_FAIL)
            return RestApiBaseResponse(**json.loads(device_response))

    def get_hs_color(self):
        """Get HS values in following format [hue, saturation].

        Return: list with hue and saturation values.
        """
        hs = [self.hsv_color[0], self.hsv_color[1]]
        return hs
    def get_hsv_color(self):
        """Get HSV color.

        Return: list with hue, saturation, value.
        """
        return self.hsv_color

    def get_brightness(self):
        """Get brightness value.

        Return: brightness.
        """
        return self.hsv_color[2]

    async def async_fetch_color_hsv(self):
        """Fetch HSV color from device.

        Return: list with hue, saturation and value. If error occured 0,0,0 will be returned.
        """
        hsv_data = await self.__device_api_client.async_get_hsv_color()
        if hsv_data.status != API_RESPONSE_STATUS_OK:
            self._state = False
            return [0, 0, 0]
        self.is_available = True
        self.hsv_color = [hsv_data.hue, hsv_data.saturation, hsv_data.value]
        return self.hsv_color

    async def async_set_brightness(self, brightness):
        """Set brightness to device.

        Keyword arguments:
        brightness -- value in range <0,100>
        """
        await self.async_set_color_hsv(value=brightness)

    async def async_set_color_hsv(self, hue = None, saturation = None, value = None):
        """Set HSV color on device.

        Keyword arguments:
        hue -- value from range <0,359>
        saturation -- value from range <0,100>
        value -- value from range <0,100>
        """
        params = {}
        if hue is not None:
            params.update({"h": int(hue) if hue < 360 else 359})
        if saturation is not None:
            params.update({"s": int(saturation)})
        if value is not None:
            params.update({"v": int(100 * ((int(value)) / 255))})
        device_response = await self.__device_api_client.async_set_hsv_color(params)
        if device_response.status != API_RESPONSE_STATUS_OK:
            self._state = False
            return

    def is_on(self, channel: int = None):
        """Return device is on status."""
        return self._state

    async def async_fetch_update(self):
        """Fetch all available data from device."""
        self._state = await self.async_fetch_channel_state()
        await self.async_fetch_color_hsv()
