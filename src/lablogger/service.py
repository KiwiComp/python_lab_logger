from collections.abc import Callable
from datetime import datetime, timezone

from lablogger.devices.base import Device
from lablogger.models import Measurement
from lablogger.storage import MeasurementRepository


class MeasurementService:
    def __init__(
        self,
        device: Device,
        repo: MeasurementRepository,
        channel: str = "cpu_temp",
        unit: str = "°C",
        alarm_threshold: float = 60.0,
        # Callback, dart --> DateTime Function().
        # A function that takes no arguments and returns the current time.
        # Injected so that tests can control time.
        clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ):
        # Dependencies and configuration
        self._device = device
        self._repo = repo
        self._channel = channel
        self._unit = unit
        self._threshold = alarm_threshold
        self._clock = clock

        # Internal state
        self._alarm_active = False

    # Dart: bool get alarmActive => _alarmActive;
    @property
    def alarm_active(self) -> bool:
        """Whether the alarm is currently active (read-only)."""
        return self._alarm_active

    def sample(self) -> Measurement:
        """Read one value, store it and update the alarm state."""
        value = self._device.read_value()
        m = Measurement(
            timestamp=self._clock(),
            channel=self._channel,
            value=value,
            unit=self._unit,
        )
        self._repo.add(m)

        alarm = value > self._threshold
        if alarm != self._alarm_active:
            self._alarm_active = alarm
            self._device.set_led(alarm)
            kind = "ALARM_ON" if alarm else "ALARM_OFF"
            self._repo.add_event(kind, f"value={value}")
        return m
