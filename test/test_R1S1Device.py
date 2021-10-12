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
    async def test_async_fetch_update(self):
        try:
            await self.device.async_fetch_update()
        except:
            self.assertFalse(True)
        self.assertTrue(True)

    def test_is_on(self):
        if not isinstance(self.device.is_on(), list):
            self.assertIn(self.device.is_on(), [True, False])

    @async_test
    async def test_turn_on(self):
        await self.device.async_set_device_state(True)
        await self.device.async_fetch_update()
        if not isinstance(self.device.is_on(), list):
            self.assertTrue(self.device.is_on())
        self.assertTrue(True)

    @async_test
    async def test_turn_off(self):
        await self.device.async_set_device_state(False)
        await self.device.async_fetch_update()
        if not isinstance(self.device.is_on(), list):
            self.assertFalse(self.device.is_on())
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()