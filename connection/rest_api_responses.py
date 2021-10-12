"""F&F Fox device responses implmentation."""

from .const import API_RESPONSE_STATUS_FAIL

class RestApiError:
    """RestApi error data holder."""

    def __init__(self, error):
        """Construct object."""
        self.error = error

class RestApiBaseResponse:
    """Base response from Fox any device."""

    def __init__(self, status: str, error: str = "", errorObj = None) -> None:
        """Construct object with status and optional error params."""
        self.status = status
        self.__has_errors = False
        if error != "" or errorObj is not None:
            self.__has_errors = True
        self.error = error
        self.__errorObj = errorObj

    def hasErrors(self) -> bool:
        """Return hasErrors flag."""
        return self.__has_errors

    def getErrorObj(self):
        """Get error object."""
        return self.__errorObj

class RestApiDeviceStateResponse(RestApiBaseResponse):
    """F&F Fox device state response."""

    def __init__(self, channel_1_state: str = None, channel_2_state: str = None,
                overcurrent: str = None, status: str = API_RESPONSE_STATUS_FAIL, state: str = None, errorObj = None) -> None:
        """Construct object with provided parameters."""
        super().__init__(status, errorObj=errorObj)
        self.state = state
		#Some of Fox devices has two channels support
        self.channel_1_state = channel_1_state
        self.channel_2_state = channel_2_state
		#Some of Fox devices has overcurrent property, we can check if device can work.
        self.overcurrent = overcurrent

class RestApiDeviceInfoResponse(RestApiBaseResponse):
    """F&F Fox device info response."""

    def __init__(self, device_name: str = "", firmware: str = "", hw: str = "",
                updater: str = "", device_friendly_name: str = "", device_commercial_name: str = "",
                status: str = API_RESPONSE_STATUS_FAIL, device_channels_name: list = None, errorObj = None) -> None:
        """Construct object with provided parameters."""
        super().__init__(status, errorObj=errorObj)
        self.device_name = device_name
        self.firmware = firmware
        self.hardware = hw
        self.updater = updater
        self.device_friendly_name = device_friendly_name
        self.device_commercial_name = device_commercial_name
        self.device_channels_name = device_channels_name

class RestApiBrightnessResponse(RestApiBaseResponse):
    """F&F Fox device brightness response."""

    def __init__(self, channel_1_value: str = None,  channel_2_value: str = None, value: str = None,
                 status: str = API_RESPONSE_STATUS_FAIL, errorObj = None) -> None:
        """Construct object with provided parameters."""
        super().__init__(status, errorObj=errorObj)
        self.brightness  = -1
        self.channel_1_value = -1
        self.channel_2_value = -1

        try:
            if value != None:
                self.brightness = int(value)
            if channel_1_value != None:
                self.channel_1_value = int(channel_1_value)
            if channel_2_value != None:
                self.channel_2_value = int(channel_2_value)
        except:
            print("Error in parsing")