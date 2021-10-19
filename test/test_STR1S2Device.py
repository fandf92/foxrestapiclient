import asyncio
from logging import error
import unittest
import sys
from os import path, wait
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from foxrestapiclient.devices.fox_str1s2_device import DeviceData, FoxSTR1S2Device
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


class STR1S2DeviceTest(unittest.TestCase):
    device = FoxSTR1S2Device(
        DeviceData(NAME, HOST, API_KEY, UNIQUE_ID, TYPE, CHANNELS)
        )

    @async_test
    async def test_set_tilt_postion(self):
        self.assertTrue(await self.device.async_set_tilt_positon(10))

    @async_test
    async def test_set_cover_postion(self):
        self.assertTrue(await self.device.async_open_cover())

if __name__ == '__main__':
    unittest.main()