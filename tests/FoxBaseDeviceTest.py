import asyncio
from logging import error
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from devices.fox_base_device import FoxBaseDevice, UnsupportedDevice

def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

class FoxBaseDeviceTest(unittest.TestCase):
    host = "192.168.0.160"
    api_key = "abf9e0f46b8f21d8ba5b86ba92"

    def test_init_base_device(self):
        try:
            FoxBaseDevice("test", self.host, self.api_key, "qwert123", 6)
        except UnsupportedDevice:
            self.assertFalse(True)
        self.assertFalse(False)

    def test_equals(self):
        self.assertEqual(FoxBaseDevice("test", self.host, self.api_key, "qwert123", 6).equals(
            FoxBaseDevice("test", self.host, self.api_key, "qwert123", 6)), True)

    def test_get_device_info(self):
        info = FoxBaseDevice("test", self.host, self.api_key, "qwert123", 6).get_device_info()
        if info != "":
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    @async_test
    async def test_async_fetch_device_available_data(self):
        """If device is not available this test will be pass"""
        dev = FoxBaseDevice("test", self.host, self.api_key, "qwert123", 6)
        await dev.async_fetch_device_available_data()

if __name__ == '__main__':
    unittest.main()