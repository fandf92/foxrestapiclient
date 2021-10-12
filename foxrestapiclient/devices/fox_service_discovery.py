"""Service discovery for F&F Fox devices."""
import asyncio
from .const import (
    DEVICES,
    DEVICE_DISCOVERY_RESPONSE_HEADER,
    DEVICE_DISCOVERY_REQUEST_HEADER,
    MIN_DATA_SIZE_TO_PARSE
)
from .fox_base_device import DeviceData
import logging
from typing import Tuple

class DeviceDiscoverProtocol(asyncio.DatagramProtocol):
    """Device disover protocol used in asyncio service discovery implementation."""

    def __init__(self, datagram_parser_callback = None) -> None:
        """Construct object."""
        super().__init__()
        self._datagram_parser_callback = datagram_parser_callback

    def connection_made(self, transport):
        """Set transport object."""
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        """Datagram reveived.

        Invoked when UDP datagram is available to read.

        Keyword arguments:
        data -- byte array response from device
        addr -- typle with sender ip address and port.

        """

        if self._datagram_parser_callback:
            self._datagram_parser_callback(data, addr)

    def error_received(self, exc):
        """Error received in UDP data."""
        logging.error("Exception thrown in UDP data receiving: %s" % exc)

class FoxServiceDiscovery:
    """Discover F&F Fox devices in local network over UDP broadcast."""

    def __init__(self) -> None:
        """Construct object."""
        self._loop = asyncio.get_running_loop()
        self._discovered_devices = []

    def get_discovered_devices(self):
        """Get dicovered devices."""
        return self._discovered_devices

    def __check_exsist_device(self, device: DeviceData):
        for dev in self._discovered_devices:
            if dev.mac_addr == device.mac_addr:
                return True
        return False

    async def async_discover_devices(self, default_tries = 5) -> list:
        """Async discovering devices.

        Send request to all devices in local network to discover them.

        Keyword arguments:
        default_tries -- default probes to discover Fox devices. This
            value extends discovering time by following formula:
            default_tries * 4 s = discovering time in seconds.

        Return: discovered devices list.
        """
        transport, protocol = await self._loop.create_datagram_endpoint(
            lambda: DeviceDiscoverProtocol(self.parse_received_datagram),
            local_addr=('0.0.0.0', 1395),
            reuse_port=True,
            allow_broadcast=True
        )
        #Clear discovered devices list.
        self._discovered_devices = []
        try:
            for i in range(default_tries):
                #Send message to UDP broadcast
                transport.sendto(DEVICE_DISCOVERY_REQUEST_HEADER.encode(), ('255.255.255.255', 1918))
                await asyncio.sleep(4)
        finally:
            transport.close()
        return self._discovered_devices

    def parse_received_datagram(self, data: bytes, addr):
        """Parse UDP message."""
        if (len(data) < MIN_DATA_SIZE_TO_PARSE):
            logging.warring("Received data size is not enough to parsing it.")
        if len(data) < len(DEVICE_DISCOVERY_RESPONSE_HEADER.encode()):
            logging.error("Parsing UDP response error. Cannot discover F&F Fox device.")
            return
        if data[0:36].decode() != DEVICE_DISCOVERY_RESPONSE_HEADER:
            logging.warning("Response not indicate to F&F Fox device.")
            return
        device_type = int.from_bytes(data[42:44], "little")
        device_unique_id = data[36:42].hex()
        try:
            discovered_device = DeviceData(
                DEVICES[device_type],
                addr[0],
                "000",
                device_unique_id,
                device_type
            )
            logging.info("Received datagram from {0}. Successfuly parsed.".format(addr))
            if self.__check_exsist_device(discovered_device) == False:
                self._discovered_devices.append(discovered_device)
        except KeyError:
            logging.error("Unsupported! F&F Fox device not implmeneted yet.")