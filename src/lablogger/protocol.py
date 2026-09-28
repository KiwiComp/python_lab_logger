from lablogger.errors import DeviceError, ProtocolError


def parse_response(line: str) -> str:
    """Parse a response line and return the payload after 'OK '."""
    line = line.strip()
    if line.startswith("OK "):
        return line[3:]
    if line.startswith("ERR "):
        raise DeviceError(line[4:])
    raise ProtocolError(f"Unexpected response: {line!r}")


def parse_value(payload: str) -> float:
    """Parse 'VALUE=48.3' into 48.3."""
    key, sep, raw = payload.partition("=")
    if key != "VALUE" or not sep:
        raise ProtocolError(f"Expected VALUE=..., got {payload!r}")
    try:
        return float(raw)
    except ValueError as exc:
        raise ProtocolError(f"Invalid number: {raw!r}") from exc
