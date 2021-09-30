import asyncio
from logging import error
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from connection.rest_api_client import RestApiClient
from connection.rest_api_responses import RestApiBaseResponse, RestApiDeviceStateResponse
from connection.const import (
    API_RESPONSE_STATUS_FAIL,
    API_RESPONSE_STATUS_OK
)
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

class RestApiClientTest(unittest.TestCase):

    host = "192.168.0.160"
    api_key = "abf9e0f46b8f21d8ba5b86ba92"

    restApiClient = RestApiClient(host, api_key)

    status_dic = [API_RESPONSE_STATUS_OK, API_RESPONSE_STATUS_FAIL]

    def test_get_base_api_url(self):
        """Test base url contatentation"""
        self.assertEqual(self.restApiClient.get_base_api_url(),
            "http://{0}/{1}/".format(self.host, self.api_key))

    def test_get_device_non_responding_response(self):
        self.assertEqual(self.restApiClient.get_device_non_responding_response().status,
            RestApiBaseResponse("false").status)

    @async_test
    async def test_async_api_get_device_state(self):
        dev_state: RestApiDeviceStateResponse = await self.restApiClient.async_api_get_device_state()
        #Device should be enabled and accessed via host and api_key to pass this test!!!
        self.assertIn(dev_state.status, self.status_dic)
        if dev_state.state is not None:
            self.assertIn(dev_state.state, ["on", "off"])
            return
        if dev_state.channel_1_state is not None and dev_state.channel_2_state is not None:
            self.assertIn(dev_state.channel_1_state, ["on", "off"])
            self.assertIn(dev_state.channel_2_state, ["on", "off"])
            return

        self.assertFalse("Unexcepted behaviour")

    @async_test
    async def test_async_api_get_device_info(self):
        dev_info = await self.restApiClient.async_api_get_device_info()
        self.assertIn(dev_info.status, self.status_dic)
        if dev_info.status == "fail":
            self.assertIsNotNone(dev_info.error)

    @async_test
    async def test_async_make_api_call_get(self):
        await self.restApiClient.async_make_api_call_get("hh")

if __name__ == '__main__':
    unittest.main()