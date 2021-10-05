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

    @async_test
    async def test_async_color_hsv(self):
        await self.device.async_set_color_hsv(100,80,70)
        await asyncio.sleep(5)
        hsv = await self.device.async_fetch_color_hsv()
        self.assertEqual(hsv[0], 100)
        self.assertEqual(hsv[1], 80)
        self.assertEqual(hsv[2], 68)

    @async_test
    async def test_async_set_brightness(self):
        await self.device.async_set_brightness(0)

if __name__ == '__main__':
    unittest.main()