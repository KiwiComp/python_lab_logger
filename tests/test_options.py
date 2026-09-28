import argparse

from lablogger.devices.simulated import SimulatedDevice
from lablogger.devices.tcp_device import TcpDevice
from lablogger.options import add_common_arguments, create_device


def parse(*argv: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    add_common_arguments(parser)
    return parser.parse_args(argv)


def test_create_device_without_host_is_simulated():
    assert isinstance(create_device(parse()), SimulatedDevice)


def test_create_device_with_host_is_tcp():
    assert isinstance(create_device(parse("--host", "localhost")), TcpDevice)


def test_common_defaults():
    args = parse()
    assert args.port == 5000
    assert args.threshold == 60.0
