"""F&F Fox devices RestAPI client. See www.fif.com.pl/fox."""
import aiohttp
from .const import (
    API_COMMON_DEVICE_OFF,
    API_COMMON_DEVICE_ON,
    API_COMMON_GET_DEVICE_INFO,
    API_COMMON_GET_STATE,
    API_COMMON_SET_STATE,
    API_CLIENT_CONNECTION_TIMEOUT,
    API_RESPONSE_STATUS_FAIL,
    REQUEST_CHANNEL_KEY,
    REQUEST_STATE_KEY,

)
import json
import logging
from .rest_api_responses import (
    RestApiBaseResponse,
    RestApiDeviceInfoResponse,
    RestApiDeviceStateResponse,
    RestApiError
)
import requests
from requests.compat import urljoin

class RestApiClient:
    """RestAPI client implmentation.

    Provides base communication with F&F Fox devices.
    F&F Fox device supports only HTTP GET request method.
    """

    def __init__(self, host: str, api_key: str):
        """Default construcring object. Host and api_key are required to make connection."""
        self._host = host
        self._api_key = api_key
        self._base_api_url = None
        self.__response_error_hook = None
        self.__session_timeout =  aiohttp.ClientTimeout(total=None,
            sock_connect=API_CLIENT_CONNECTION_TIMEOUT, sock_read=API_CLIENT_CONNECTION_TIMEOUT)

    def register_response_error_hook(self, response_hook):
        """Register response error hook."""
        self.__response_error_hook = response_hook

    def unregister_response_error_hook(self):
        """Unregister response error hook."""
        self.__response_error_hook = None

    def get_base_api_url(self) -> str:
        """Create base_api_url if needed and return it."""
        if self._base_api_url is not None:
            return self._base_api_url
        #Fox device working with rest api key. This key must exsist in url in below format.
        url_pattern = "http://{0}/{1}/"
        self._base_api_url = url_pattern.format(self._host, self._api_key)
        return self._base_api_url

    async def async_api_get_device_state(self, channel = None) -> RestApiDeviceStateResponse:
        """Get F&F Fox device state.

        Make HTTP GET request to device and get state.
        Keyword arguments:
        channel -- optional, get state from provided channel

        Return: RestApiDeviceStateResponse
        """
        params = {}
        if channel is not None:
            params = {REQUEST_CHANNEL_KEY: channel}
        logging.info("Making call in async_api_get_device_state().")
        response_content = await self.async_make_api_call_get(API_COMMON_GET_STATE, params)
        if response_content is None:
            return RestApiDeviceStateResponse(status=API_RESPONSE_STATUS_FAIL)
        if isinstance(response_content, RestApiError):
            return RestApiDeviceStateResponse(API_RESPONSE_STATUS_FAIL, errorObj=response_content)
        return RestApiDeviceStateResponse(**json.loads(response_content))

    async def async_api_set_device_state(self, state, channel = None) -> RestApiBaseResponse:
        """Set F&F Fox device state.

        Make HTTP GET request to device and set state
        Keyword arguments:
        state -- state to set on device can be true or false - it will be marked to on/off
        channel -- optional, set state on provided channel

        Return: RestApiBaseResponse
        """
        params = {
            REQUEST_STATE_KEY: API_COMMON_DEVICE_ON if state == True else API_COMMON_DEVICE_OFF
        }
        if channel is not None:
            params.update({REQUEST_CHANNEL_KEY: channel})
        logging.info("Making call in async_api_set_device_state() with params {0}.".format(params))
        response_content = await self.async_make_api_call_get(API_COMMON_SET_STATE, params)
        if response_content is None:
            return RestApiBaseResponse(API_RESPONSE_STATUS_FAIL)
        if isinstance(response_content, RestApiError):
            return RestApiBaseResponse(API_RESPONSE_STATUS_FAIL, errorObj=response_content)
        return RestApiBaseResponse(**json.loads(response_content))

    async def async_api_get_device_info(self) -> RestApiDeviceInfoResponse:
        """Get F&F Fox device info.

        Get device information such as firmware version, name etc.
        See RestApiDeviceInfoResponse to check what data is returnig from device.
        """
        logging.info("Making call in async_api_get_device_info().")
        response_content = await self.async_make_api_call_get(API_COMMON_GET_DEVICE_INFO)
        if response_content is None:
            return RestApiDeviceInfoResponse(status=API_RESPONSE_STATUS_FAIL)
        if isinstance(response_content, RestApiError):
            return RestApiDeviceInfoResponse(status=API_RESPONSE_STATUS_FAIL, errorObj=response_content)
        return RestApiDeviceInfoResponse(**json.loads(response_content))

    async def async_make_api_call_get(self, method: str, query_params = None):
        """Make HTTP GET request by given parameters.

        Keyword arguments:
        method -- method name to make request
        query_params - optional request parameters
        """
        if not isinstance(method, str):
            logging.warning("Wrong argument passed to method. Http method accept only string values.")
            return
        if query_params is not None and not isinstance(query_params, dict):
            logging.warning("Wrong argument passed to method. Query params must be dict.")
            return
        try:
            async with aiohttp.ClientSession(timeout = self.__session_timeout) as session:
                async with session.get(urljoin(self.get_base_api_url(), method), params=query_params) as resp:
                    response = await resp.read()
                    logging.info("Received RAW response {0}".format(response))
                    self.__invoke_response_error_hook(None) #Raise reponse_error_hook with None errors.
                    return response
        except aiohttp.ClientConnectionError as e:
            logging.error(e)
            self.__invoke_response_error_hook(e)
        except requests.exceptions.RequestException as e:
            logging.error(e)
            self.__invoke_response_error_hook(e)
        return None

    def __invoke_response_error_hook(self, e):
        """Invoke response error hook if registered."""
        if self.__response_error_hook != None:
                self.__response_error_hook(e)