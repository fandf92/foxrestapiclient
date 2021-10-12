import asyncio
from logging import error
import unittest
import sys
from os import path, wait
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from foxrestapiclient.devices.fox_service_discovery import FoxServiceDiscovery

def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

class ServiceDiscoveryTest(unittest.TestCase):

    @async_test
    async def test(self):
        discovered = await FoxServiceDiscovery().async_discover_devices()
        if len(discovered) == 0:
            self.assertFalse(True)
        for device in discovered:
            self.assertIsNotNone(device.name)

if __name__ == '__main__':
    unittest.main()