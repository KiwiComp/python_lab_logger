import socket

from lablogger.devices.base import Device
from lablogger.errors import DeviceError
from lablogger.protocol import parse_response, parse_value


class TcpDevice(Device):  # Inherits device.
    def __init__(self, host: str, port: int = 5000, timeout: float = 1.0):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._sock: socket.socket | None = None
        self._file = None

    def connect(self) -> None:
        try:
            self._sock = socket.create_connection(
                (self._host, self._port), timeout=self._timeout
            )
        except OSError as exc:
            raise DeviceError(
                f"Could not connect to {self._host}:{self._port}: {exc}"
            ) from exc
        self._file = self._sock.makefile("rwb")
        try:
            if self._send(command="PING") != "PONG":
                raise DeviceError("Device did not answer PING")
        except Exception:
            self.close()  # __exit__ does not run if __enter__ fails
            raise

    def close(self) -> None:
        # Order is important: _file is layer upon _sock and should be closed first.
        if self._file is not None:
            self._file.close()
            self._file = None
        if self._sock is not None:
            self._sock.close()
            self._sock = None

    def read_value(self) -> float:
        return parse_value(payload=self._send(command="READ"))

    def set_led(self, on: bool) -> None:
        state = 1 if on else 0
        if self._send(command=f"LED {state}") != f"LED={state}":
            raise DeviceError("Device did not confirm LED state")

    def _send(self, command: str) -> str:
        if self._file is None:
            raise DeviceError("Not connected")
        try:
            # Write to instrument. "READ" becomes b"READ\n". encode converts text to bytes.
            self._file.write((command + "\n").encode("ascii"))
            # Send the buffered bytes now instead of waiting for the buffer to fill.
            self._file.flush()
            # Wait for one complete response line, at most until the timeout.
            raw = self._file.readline()
        except TimeoutError as exc:  # must come before OSError, its parent class
            raise DeviceError(f"Timeout: no response to {command!r}") from exc
        except OSError as exc:
            raise DeviceError(f"Communication error: {exc}") from exc
        if not raw:
            raise DeviceError("Connection closed by device")
        # raw content is bytes, convert to string through decode.
        # Invalid ASCII bytes become "?" instead of raising, so garbled data
        # ends up as a clear ProtocolError from parse_response.
        return parse_response(line=raw.decode("ascii", errors="replace"))
