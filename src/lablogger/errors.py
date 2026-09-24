# Dart --> class LabLoggerError implements Exception { ... }
class LabLoggerError(Exception):
    """Base class for all LabLogger errors."""

# Dart --> class ProtocolError extends LabLoggerError { ... }
class ProtocolError(LabLoggerError):
    """The device response does not follow the protocol."""

# Dart --> class DeviceError extends LabLoggerError { ... }
class DeviceError(LabLoggerError):
    """The device reported an error or did not respond."""