import asyncio
from logging import error
import unittest
import sys
from os import path, wait
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from foxrestapiclient.devices.fox_led2s2_device import DeviceData, FoxLED2S2Device
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
    device = FoxLED2S2Device(
        DeviceData(NAME, HOST, API_KEY, UNIQUE_ID, TYPE, CHANNELS)
        )

    @async_test
    async def test_turn_off(self):
        await self.device.async_update_channel_state(False, 1)
        await self.device.async_update_channel_state(False, 2)
        await self.device.async_fetch_update()
        await asyncio.sleep(1)

    @async_test
    async def test_turn_on(self):
        await self.device.async_update_channel_state(True, 1)
        await self.device.async_update_channel_state(True, 2)
        await self.device.async_fetch_update()
        await asyncio.sleep(1)

    @async_test
    async def test_async_update_channel_brightness(self):
        await self.device.async_update_channel_brightness(47, 1)
        await asyncio.sleep(5)
        await self.device.async_update_channel_brightness(76, 2)
        await asyncio.sleep(5)
        await self.device.async_fetch_update()
        await asyncio.sleep(5)
        self.assertEqual(self.device.channel_one_brightness, 47)
        self.assertEqual(self.device.channel_two_brightness, 76)

    @async_test
    async def test_async_fetch_channel_one_state(self):
        self.assertTrue(await self.device.async_fetch_channel_one_state())

    @async_test
    async def test_async_fetch_update(self):
        await self.device.async_fetch_update()


if __name__ == '__main__':
    unittest.main()