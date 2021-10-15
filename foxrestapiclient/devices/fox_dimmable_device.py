"""Fox dimmable device implementation."""

import logging
from .fox_base_device import DeviceData, FoxBaseDevice
from foxrestapiclient.connection.rest_api_client import RestApiClient
from foxrestapiclient.connection.rest_api_responses import RestApiBaseResponse, RestApiBrightnessResponse
from foxrestapiclient.connection.const import (
    API_RESPONSE_STATUS_FAIL,
    API_RESPONSE_STATUS_INVALID,
    REQUEST_CHANNEL_KEY
)
from .const import (
    API_DIMMABLE_GET_BRIGHTNESS,
    API_DIMMABLE_SET_BRIGHTNESS,
)
import json

class FoxDimmableDevice(FoxBaseDevice):
    """Fox Dimmable device implementation. Base class for any device with dimmable feature."""

    def __init__(self, device_data: DeviceData):
        """Initialize object."""
        super().__init__(device_data.name, device_data.host, device_data. api_key,
                        device_data.mac_addr, device_data.type)
        #Extened RestApi methods, specific for device
        self.__device_api_client = self.__DeviceRestApiImplementer(super())

    class __DeviceRestApiImplementer:
        """Inner class with specific RestApi methods definition used by device."""

        def __init__(self, restApiClient: RestApiClient) -> None:
            """Initialize object."""
            self._restApiClient = restApiClient

        async def async_get_brightness_value(self, params) -> RestApiBrightnessResponse:
            """Get brightness value by given channel.

            Keyword arguments:
            params -- params dictionary, should contain channel number
            Return:
            RestApiBrightnessResponse
            """
            device_response = await self._restApiClient.async_make_api_call_get(
                API_DIMMABLE_GET_BRIGHTNESS, params)
            if device_response is None:
                return RestApiBrightnessResponse(status=API_RESPONSE_STATUS_FAIL)
            return RestApiBrightnessResponse(**json.loads(device_response))

        async def async_set_brighntess_value(self, params) -> RestApiBaseResponse:
            """Set brightness value.

            Keyword arguments:
            params -- params dictionary, should contain channel number
            Return:
            RestApiBaseResponse
            """
            device_response = await self._restApiClient.async_make_api_call_get(
                API_DIMMABLE_SET_BRIGHTNESS, params)
            if device_response is None:
                return RestApiBaseResponse(API_RESPONSE_STATUS_FAIL)
            return RestApiBaseResponse(**json.loads(device_response))

    async def async_fetch_channel_brightness(self, channel: int = 0) -> list:
        """Fetch device brightness value by given channel.

        If channel number not provided fetch brightness from all channels.

        Keyword arguments:
        channel -- channel number
        Return:
        list(int) -- readed values.
        """
        params = None
        if channel != 0:
            params = {
                REQUEST_CHANNEL_KEY: str(channel)
            }
        device_response = await self.__device_api_client.async_get_brightness_value(params)
        if (device_response.status == API_RESPONSE_STATUS_FAIL or
            device_response.status == API_RESPONSE_STATUS_INVALID):
            return [0,0]
        values = []
        if device_response.brightness != -1:
            values.append(device_response.brightness)
        if device_response.channel_1_value != -1:
            values.append(device_response.channel_1_value)
        if device_response.channel_2_value != -1:
            values.append(device_response.channel_2_value)
        return values

    async def async_update_channel_brightness(self, brightness: int, channel: int = None):
        """Set brightness value on device.

        Keyword arguments:
        brightness -- value from range <0-255>
        channel -- value from range <1-2> or None.
        """
        if brightness < 0 or brightness > 255:
            logging.warning("Brightness passed to sync_update_channel_brightness() is out of range.")
            return
        if channel is not None and (channel < 0 or channel > 2):
            logging.warning("Channel passed to sync_update_channel_brightness() is out of range.")
            return
        params = {
            "value": brightness, #Will be removed in next version.
        }
        if channel is not None:
            params.update({REQUEST_CHANNEL_KEY: channel})
        device_response = await self.__device_api_client.async_set_brighntess_value(params)
        if (device_response.status == API_RESPONSE_STATUS_FAIL or
            device_response.status == API_RESPONSE_STATUS_INVALID):
            logging.error("Setting brightness value in async_update_channel_brightness() failed.")