"""F&F Fox Energy device implementation."""

import json

from foxrestapiclient.connection.const import API_RESPONSE_STATUS_FAIL
from foxrestapiclient.connection.rest_api_client import RestApiClient
from foxrestapiclient.connection.rest_api_responses import RestApiBaseResponse

from .const import API_ENERGY_GET_CURRENT_PARAMETERS, API_ENERGY_GET_TOTAL_ENERGY
from .fox_base_device import DeviceData, FoxBaseDevice


class FoxEnergyDevice(FoxBaseDevice):
    """F&F Fox ENERGY device. Energy meter."""

    def __init__(self, device_data: DeviceData):
        """Initialize object by given device data."""
        super().__init__(device_data)
        self.__device_api_client = self.DeviceRestApiImplementer(self._rest_api_client)
        self.has_sensor_data = True
        self._state = False
        self.total_energy_data = self.TotalEnergySensorData()
        self.current_parameters_data = self.CurrentParamsSensorData()
        self.__init_all_sensor_values()

    class TotalEnergySensorData(RestApiBaseResponse):
        """Energy sensor data holder."""

        def __init__(self, active_energy_export: list = [None for i in range(3)], reactive_energy_export: list = [None for i in range(3)],
                active_energy_import: list = [None for i in range(3)], reactive_energy_import: list = [None for i in range(3)],
                status: str = API_RESPONSE_STATUS_FAIL) -> None:
            """Initialize obiect."""
            super().__init__(status)
            self.active_energy_export = active_energy_export
            self.reactive_energy_export = reactive_energy_export
            self.active_energy_import = active_energy_import
            self.reactive_energy_import = reactive_energy_import

    class CurrentParamsSensorData(RestApiBaseResponse):
        """Energy Parameters data holder."""

        def __init__(self, voltage: list = [None for i in range(3)], current: list = [None for i in range(3)], power_active: list = [None for i in range(3)],
                    power_reactive: list = [None for i in range(3)], frequency: list = [None for i in range(3)], power_factor: list = [None for i in range(3)],
                    status: str = API_RESPONSE_STATUS_FAIL) -> None:
            """Initialize obiect."""
            super().__init__(status)
            self.voltage = voltage
            self.current = current
            self.power_active = power_active
            self.power_reactive = power_reactive
            self.frequency = frequency
            self.power_factor = power_factor

    class DeviceRestApiImplementer:
        """RestAPI methods definition used by Fox Energy device."""

        def __init__(self, rest_api_client: RestApiClient) -> None:
            """Initialize obiect."""
            self._rest_api_client = rest_api_client

        async def async_fetch_current_parameters_data(self):
            """Fetch energy parametrs from device.

            Get information about electricty network such as voltage, current etc.
            see ACParamsSensorData to show what data can be readed.
            """
            device_response = (
                await self._rest_api_client.async_make_api_call_get(API_ENERGY_GET_CURRENT_PARAMETERS)
            )
            if device_response is None:
                return FoxEnergyDevice.CurrentParamsSensorData(status=API_RESPONSE_STATUS_FAIL)
            return FoxEnergyDevice.CurrentParamsSensorData(**json.loads(device_response))

        async def async_fetch_total_energy_data(self):
            """Fetch total energy parametrs from device."""
            device_response = (
                await self._rest_api_client.async_make_api_call_get(API_ENERGY_GET_TOTAL_ENERGY)
            )
            if device_response is None:
                return FoxEnergyDevice.TotalEnergySensorData(status=API_RESPONSE_STATUS_FAIL)
            return FoxEnergyDevice.TotalEnergySensorData(**json.loads(device_response))

    def __init_all_sensor_values(self):
        """Initialize all sensor values JSON string."""
        self.all_sensor_values = {
            "voltage": self.current_parameters_data.voltage,
            "current": self.current_parameters_data.current,
            "power_active": self.current_parameters_data.power_active,
            "power_reactive": self.current_parameters_data.power_reactive,
            "frequency": self.current_parameters_data.frequency,
            "power_factor": self.current_parameters_data.power_factor,
            "active_energy_export": self.total_energy_data.active_energy_export,
            "reactive_energy_export": self.total_energy_data.reactive_energy_export,
            "active_energy_import": self.total_energy_data.active_energy_import,
            "reactive_energy_import": self.total_energy_data.reactive_energy_import,
        }

    def fetch_sensor_value_by_key(self, key: str):
        """Fetch readed value from device by key.

        If key not exist NaN str will be returned.

        Keyword arguments:
        key -- related value by key.
        Return:
        returned value by provided key.
        """
        try:
            return self.all_sensor_values[key]
        except KeyError:
            return "NaN"

    def get_all_electricty_data(self) -> dict:
        """Get all readed data from electricty sensor as dictionary."""
        return self.all_sensor_values

    async def async_fetch_update(self):
        """Fetch all available data from device."""
        self._state = await self.async_fetch_channel_state()
        self.total_energy_data = await self.__device_api_client.async_fetch_total_energy_data()
        self.current_parameters_data = await self.__device_api_client.async_fetch_current_parameters_data()
        self.__init_all_sensor_values()
