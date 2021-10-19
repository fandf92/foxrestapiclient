import asyncio
from logging import error
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from foxrestapiclient.devices.fox_base_device import FoxBaseDevice, UnsupportedDevice
from .const import (
    API_KEY,
    HOST,
    NAME,
    TYPE,
    UNIQUE_ID
)
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

class FoxBaseDeviceTest(unittest.TestCase):
    device = FoxBaseDevice(NAME, HOST, API_KEY, UNIQUE_ID, TYPE)

    def test_equals(self):
        self.assertTrue(self.device.equals(
            FoxBaseDevice(NAME, HOST, API_KEY, UNIQUE_ID, TYPE)))

    def test_get_channel_name(self):
        self.assertIsNotNone(self.device.get_channel_name(0))
        self.assertIsNotNone(self.device.get_channel_name(1))
        self.assertIsNotNone(self.device.get_channel_name(2))
        self.assertIsNotNone(self.device.get_channel_name(10))
        self.assertIsNotNone(self.device.get_channel_name(-1))

    def test_get_device_info(self):
        device_info = self.device.get_device_info()
        self.assertIsNotNone(device_info["identifiers"])
        self.assertIsNotNone(device_info["name"])
        self.assertIsNotNone(device_info["manufacturer"])
        self.assertIsNotNone(device_info["model"])
        self.assertIsNotNone(device_info["sw_version"])

    @async_test
    async def test_async_fetch_channel_state(self):
        state = await self.device.async_fetch_channel_state()
        self.assertIn(state, [True, False])

    @async_test
    async def test_async_update_channel_state(self):
        self.assertTrue((await self.device.async_update_channel_state(False)))

    @async_test
    async def test_async_fetch_device_info(self):
        self.assertTrue((await self.device.async_fetch_device_info()))

if __name__ == '__main__':
    unittest.main()