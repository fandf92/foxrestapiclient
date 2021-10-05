"""F&F Fox R1S1 device implementation."""

from .fox_base_device import DeviceData, FoxBaseDevice
from foxrestapiclient.connection.rest_api_client import RestApiClient
from foxrestapiclient.connection.rest_api_responses import RestApiBaseResponse
from foxrestapiclient.connection.const import (
    API_RESPONSE_STATUS_FAIL,
)
from .const import (
    API_R1S1_GET_AC_PARAMETERS,
    API_R1S1_GET_TOTAL_ENERGY_DATA
)
import json


class FoxR1S1Device(FoxBaseDevice):
    """F&F Fox R1S1 device. Single switch, relay with energy meter."""

    def __init__(self, device_data: DeviceData):
        """Initialize object by given device data."""
        super().__init__(device_data.name, device_data.host, device_data.api_key,
                        device_data.mac_addr, device_data.type)
        self.__device_api_client = self.DeviceRestApiImplementer(super())
        self.has_sensor_data = True
        self.total_energy_data = self.EnergySensorData
        self.ac_parameters_data = self.ACParamsSensorData

    class EnergySensorData(RestApiBaseResponse):
        """Energy sensor data holder."""

        def __init__(self, active_energy: str = None, reactive_energy: str = None, active_energy_import: str = None,
                    reactive_energy_import: str = None, status: str = API_RESPONSE_STATUS_FAIL) -> None:
            """Initialize obiect."""
            super().__init__(status)
            self.active_energy = active_energy
            self.reactive_energy = reactive_energy
            self.active_energy_import = active_energy_import
            self.reactive_energy_import = reactive_energy_import

    class ACParamsSensorData(RestApiBaseResponse):
        """AC Parameters data holder."""

        def __init__(self, voltage: str = None, current: str = None, power_active: str = None,
                    power_reactive: str = None, frequency: str = None, power_factor: str = None,
                    status: str = API_RESPONSE_STATUS_FAIL) -> None:
            """Initialize obiect."""
            super().__init__(status)
            self.voltage = voltage
            self.current = current
            self.power_active = power_active
            self.power_reactive = power_reactive
            self.frequency = frequency
            self.power_factor = power_factor

    class DeviceRestApiImplementer(RestApiClient):
        """RestAPI methods definition used by Fox R1S1 device."""

        def __init__(self, restApiClient: RestApiClient) -> None:
            """Initialize obiect."""
            self._restApiClient = restApiClient

        async def async_fetch_ac_parameters_data(self):
            """Fetch AC parametrs from device.

            Get information about electricty network such as voltage, current etc.
            see ACParamsSensorData to show what data can be readed.
            """
            device_response = await self._restApiClient.async_make_api_call_get(API_R1S1_GET_AC_PARAMETERS)
            if device_response is None:
                return FoxR1S1Device.ACParamsSensorData(status=API_RESPONSE_STATUS_FAIL)
            return FoxR1S1Device.ACParamsSensorData(**json.loads(device_response))

        async def async_fetch_total_energy_data(self):
            """Fetch total energy parametrs from device."""
            device_response = await self._restApiClient.async_make_api_call_get(API_R1S1_GET_TOTAL_ENERGY_DATA)
            if device_response is None:
                return FoxR1S1Device.EnergySensorData(status=API_RESPONSE_STATUS_FAIL)
            return FoxR1S1Device.EnergySensorData(**json.loads(device_response))

    def fetch_sensor_value_by_key(self, key: str):
        """Fetch readed value from device by key.

        If key not exist NaN str will be returned.

        Keyword arguments:
        key -- related value by key.
        Return:
        returned value by provided key.
        """
        self.all_sensor_values = {
            "voltage": self.ac_parameters_data.voltage,
            "current": self.ac_parameters_data.current,
            "power_active": self.ac_parameters_data.power_active,
            "power_reactive": self.ac_parameters_data.power_reactive,
            "frequency": self.ac_parameters_data.frequency,
            "power_factor": self.ac_parameters_data.power_factor,
            "active_energy": self.total_energy_data.active_energy,
            "reactive_energy": self.total_energy_data.reactive_energy,
            "active_energy_import": self.total_energy_data.active_energy_import,
            "reactive_energy_import": self.total_energy_data.reactive_energy_import,
        }
        try:
            return self.all_sensor_values[key]
        except KeyError:
            return "NaN"

    def get_all_electricty_data(self) -> dict:
        """Get all readed data from electricty sensor as dictionary."""
        return self.all_sensor_values

    def is_on(self, channel: int = None):
        """Return device is on status."""
        return self._state

    async def async_fetch_update(self):
        """Fetch all available data from device."""
        self._state = await self.async_fetch_channel_state()
        self.total_energy_data = await self.__device_api_client.async_fetch_total_energy_data()
        self.ac_parameters_data = await self.__device_api_client.async_fetch_ac_parameters_data()