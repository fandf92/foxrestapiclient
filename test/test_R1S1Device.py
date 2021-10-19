import asyncio
from logging import error
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from foxrestapiclient.devices.fox_r1s1_device import DeviceData, FoxR1S1Device
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

class R1S1DeviceTest(unittest.TestCase):
    device = FoxR1S1Device(
        DeviceData(NAME, HOST, API_KEY, UNIQUE_ID, TYPE, CHANNELS)
        )

    @async_test
    async def test_turn_on(self):
        self.assertTrue(await self.device.async_update_channel_state(True))

    @async_test
    async def test_turn_off(self):
        self.assertTrue(await self.device.async_update_channel_state(False))

    @async_test
    async def test_fetch_sensor_value_by_key(self):
        await self.device.async_fetch_update()
        self.assertIsNone(self.device.fetch_sensor_value_by_key("voltage"))

if __name__ == '__main__':
    unittest.main()