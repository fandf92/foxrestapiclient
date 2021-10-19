import asyncio
from logging import error
import unittest
import sys
from os import path, wait
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from foxrestapiclient.devices.fox_dim1s2_device import DeviceData, FoxDIM1S2Device
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

class DIM1S2DeviceTest(unittest.TestCase):
    device = FoxDIM1S2Device(
        DeviceData(NAME, HOST, API_KEY, UNIQUE_ID, TYPE, CHANNELS)
        )

    @async_test
    async def test_turn_off(self):
        self.assertTrue(await self.device.async_update_channel_state(False))

    @async_test
    async def test_turn_on(self):
        self.assertTrue(await self.device.async_update_channel_state(True))

    @async_test
    async def test_async_update_channel_brightness(self):
        await self.device.async_update_channel_brightness(50)
        await asyncio.sleep(5)
        await self.device.async_fetch_update()
        self.assertEqual(self.device.brightness, 50)

    # @async_test
    # async def test_async_fetch_channel_one_state(self):
    #     self.assertTrue(await self.device.async_fetch_channel_one_state())

    # @async_test
    # async def test_async_fetch_update(self):
    #     await self.device.async_fetch_update()


if __name__ == '__main__':
    unittest.main()