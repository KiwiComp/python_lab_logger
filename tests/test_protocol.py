import pytest

from lablogger.errors import DeviceError, ProtocolError
from lablogger.protocol import parse_response, parse_value


def test_parse_response_ok():
    """Verifies REQ-001."""
    assert parse_response("OK VALUE=48.3\r\n") == "VALUE=48.3"


def test_parse_response_device_error():
    """Verifies REQ-006."""
    with pytest.raises(DeviceError):
        parse_response("ERR UNKNOWN_COMMAND")


@pytest.mark.parametrize("bad", ["", "HELLO", "OKVALUE=1"])
def test_parse_response_garbage(bad):
    """Verifies REQ-006."""
    with pytest.raises(ProtocolError):
        parse_response(bad)


def test_parse_value():
    """Verifies REQ-001."""
    assert parse_value("VALUE=48.3") == 48.3


def test_parse_value_invalid_number():
    """Verifies REQ-006."""
    with pytest.raises(ProtocolError):
        parse_value("VALUE=abc")
