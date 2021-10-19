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
    async def test_turn_on(self):
        self.assertTrue(await self.device.async_update_channel_state(True,1))

    @async_test
    async def test_turn_off(self):
        self.assertTrue(await self.device.async_update_channel_state(False,2))


if __name__ == '__main__':
    unittest.main()