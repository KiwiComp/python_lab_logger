from lablogger.devices.base import Device
from lablogger.service import MeasurementService
from lablogger.storage import MeasurementRepository


class FakeDevice(Device):
    def __init__(self, values):
        self._values = iter(values)
        self.led_calls = []

    def connect(self):
        pass

    def close(self):
        pass

    def read_value(self):
        return next(self._values)

    def set_led(self, on):
        self.led_calls.append(on)


def test_alarm_turns_led_on_then_off():
    """Verifies REQ-003 and REQ-004."""
    device = FakeDevice([45.0, 65.0, 70.0, 50.0])
    repo = MeasurementRepository(":memory:")
    service = MeasurementService(device, repo, alarm_threshold=60.0)

    for _ in range(4):
        service.sample()

    assert device.led_calls == [True, False]
    assert [kind for _, kind, _ in repo.events()] == ["ALARM_ON", "ALARM_OFF"]
    assert len(repo.latest()) == 4
