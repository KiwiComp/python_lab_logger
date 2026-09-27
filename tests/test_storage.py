from datetime import UTC, datetime

from lablogger.models import Measurement
from lablogger.storage import MeasurementRepository


def test_add_and_read_back():
    """Verifies REQ-002."""
    repo = MeasurementRepository(":memory:")
    timestamp = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    m = Measurement(timestamp, "cpu_temp", 48.3, "°C")
    repo.add(m)
    assert repo.latest() == [m]


def test_latest_respects_limit_and_order():
    repo = MeasurementRepository(":memory:")
    for i in range(5):
        timestamp = datetime(2026, 1, 1, 12, i, tzinfo=UTC)
        repo.add(Measurement(timestamp, "cpu_temp", float(i), "°C"))
    assert [m.value for m in repo.latest(limit=2)] == [3.0, 4.0]
