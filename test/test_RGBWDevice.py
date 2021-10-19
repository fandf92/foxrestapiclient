import asyncio
from logging import error
import unittest
import sys
from os import path, wait
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from foxrestapiclient.devices.fox_rgbw_device import DeviceData, FoxRGBWDevice
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


class RGBWDeviceTest(unittest.TestCase):
    device = FoxRGBWDevice(
        DeviceData(NAME, HOST, API_KEY, UNIQUE_ID, TYPE, CHANNELS)
        )

    def test_get_hs_color(self):
        self.assertIsInstance(self.device.get_hs_color(), list)

    def test_get_hsv_color(self):
        self.assertIsInstance(self.device.get_hsv_color(), list)

    def test_get_brightness(self):
        self.assertIsInstance(self.device.get_brightness(), int)

    @async_test
    async def test_async_fetch_color_hsv(self):
        self.assertIsNot(await self.device.async_fetch_color_hsv(), [0,0,0])

    @async_test
    async def test_async_set_brightness(self):
        self.assertTrue(await self.device.async_set_brightness(43))

    @async_test
    async def test_async_set_color_hsv(self):
        self.assertTrue(await self.device.async_set_color_hsv(359, 80, 20))

    @async_test
    async def test_update(self):
        await self.device.async_fetch_update()

if __name__ == '__main__':
    unittest.main()