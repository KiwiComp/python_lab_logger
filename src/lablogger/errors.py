class LabLoggerError(Exception):
    """Base class for all LabLogger errors."""


class ProtocolError(LabLoggerError):
    """The device response does not follow the protocol."""


class DeviceError(LabLoggerError):
    """The device reported an error or did not respond."""
