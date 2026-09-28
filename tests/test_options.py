import argparse

from lablogger.devices.simulated import SimulatedDevice
from lablogger.devices.tcp_device import TcpDevice
from lablogger.options import add_common_arguments, create_device


def parse(*argv: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    add_common_arguments(parser)
    return parser.parse_args(argv)


def test_create_device_without_host_is_simulated():
    """Verifies REQ-005."""
    assert isinstance(create_device(parse()), SimulatedDevice)


def test_create_device_with_host_is_tcp():
    """Verifies REQ-001."""
    assert isinstance(create_device(parse("--host", "localhost")), TcpDevice)


def test_common_defaults():
    args = parse()
    assert args.port == 5000
    assert args.threshold == 60.0


def test_common_arguments_can_be_set():
    """Verifies REQ-007."""
    args = parse(
        "--host",
        "192.168.1.42",
        "--port",
        "6000",
        "--db",
        "test.db",
        "--threshold",
        "3000",
        "--channel",
        "potentiometer",
        "--unit",
        "raw",
    )
    assert args.host == "192.168.1.42"
    assert args.port == 6000
    assert args.db == "test.db"
    assert args.threshold == 3000.0
    assert args.channel == "potentiometer"
    assert args.unit == "raw"
