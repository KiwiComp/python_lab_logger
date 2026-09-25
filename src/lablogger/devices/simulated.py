import math
import random
import time

from lablogger.devices.base import Device
from lablogger.errors import DeviceError


class SimulatedDevice(Device): # Inherits Device.
    """Simulates a temperature that follows a sine wave with noise."""

    def __init__(self, noise: float = 0.5, seed: int | None = None):
        self._rng = random.Random(seed)
        self._noise = noise
        self._start = time.monotonic()
        self._connected = False
        self.led_on = False

    def connect(self) -> None:
        self._connected = True
    
    def close(self) -> None:
        self._connected = False
    
    def read_value(self) -> float:
        if not self._connected:
            raise DeviceError("Not connected")
        t = time.monotonic() - self._start
        base = 50 + 15 * math.sin(t / 10)
        return round(base + self._rng.gauss(0, self._noise), 1)
    
    def set_led(self, on: bool) -> None:
        self.led_on = on
    