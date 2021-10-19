import asyncio
from logging import error
import unittest
import sys
from os import path, wait
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from foxrestapiclient.devices.fox_dimmable_device import DeviceData, FoxDimmableDevice
from .const import (
    API_KEY,
    CHANNELS,
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

class DimmableDeviceTest(unittest.TestCase):
    device = FoxDimmableDevice(
        DeviceData(NAME, HOST, API_KEY, UNIQUE_ID, TYPE, CHANNELS)
        )

    @async_test
    async def test_async_fetch_channel_brightness(self):
        self.assertIsInstance(
            await self.device.async_fetch_channel_brightness(),
            list
        )

    @async_test
    async def test_async_update_channel_brightness(self):
        self.assertTrue(await self.device.async_update_channel_brightness(255, 2))

    @async_test
    async def test_async_update_channel_state(self):
        self.assertTrue(await self.device.async_update_channel_state(False, 9))

if __name__ == '__main__':
    unittest.main()