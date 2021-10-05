import asyncio
from logging import error
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from foxrestapiclient.devices.fox_base_device import FoxBaseDevice, UnsupportedDevice
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

class FoxBaseDeviceTest(unittest.TestCase):
    def test_init_base_device(self):
        try:
            FoxBaseDevice(NAME, HOST, API_KEY, UNIQUE_ID, TYPE)
        except UnsupportedDevice:
            self.assertFalse(True)
        self.assertFalse(False)

    def test_equals(self):
        self.assertEqual(FoxBaseDevice(NAME, HOST, API_KEY, UNIQUE_ID, TYPE).equals(
            FoxBaseDevice(NAME, HOST, API_KEY, UNIQUE_ID, TYPE)), True)

    def test_get_device_info(self):
        info = FoxBaseDevice(NAME, HOST, API_KEY, UNIQUE_ID, TYPE).get_device_info()
        if info != "":
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    @async_test
    async def test_async_fetch_device_available_data(self):
        """If device is not available this test will be pass"""
        dev = FoxBaseDevice(NAME, HOST, API_KEY, UNIQUE_ID, TYPE)
        await dev.async_fetch_device_available_data()

if __name__ == '__main__':
    unittest.main()