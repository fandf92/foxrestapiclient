import asyncio
from logging import error
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from foxrestapiclient.devices.fox_r2s2_device import DeviceData, FoxR2S2Device
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

class R2S2DeviceTest(unittest.TestCase):
    device = FoxR2S2Device(
        DeviceData(NAME, HOST, API_KEY, UNIQUE_ID, TYPE, CHANNELS)
        )

    @async_test
    async def test_async_fetch_update(self):

        try:
            await self.device.async_fetch_update()
        except:
            self.assertFalse(True)
        self.assertTrue(True)

    def test_is_on(self):
        self.assertIn(self.device.is_on(2), [True, False])

if __name__ == '__main__':
    unittest.main()