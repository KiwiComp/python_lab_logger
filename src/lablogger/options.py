import argparse

from lablogger.devices.base import Device
from lablogger.devices.simulated import SimulatedDevice
from lablogger.devices.tcp_device import TcpDevice


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the options shared by the CLI and the GUI."""
    parser.add_argument(
        "--host",
        help="Instrument address, e.g. lablogger-pi.local or 192.168.1.42. "
        "Omit for simulation.",
    )
    parser.add_argument("--port", type=int, default=5000, help="Instrument TCP port")
    parser.add_argument("--db", default="lablogger.db", help="SQLite database file")
    parser.add_argument("--threshold", type=float, default=60.0, help="Alarm threshold")
    parser.add_argument(
        "--channel", default="cpu_temp", help="Channel name stored with each value"
    )
    parser.add_argument("--unit", default="°C", help="Unit stored with each value")


def create_device(args: argparse.Namespace) -> Device:
    """Return a TcpDevice if --host is given, otherwise a SimulatedDevice."""
    if args.host:
        return TcpDevice(host=args.host, port=args.port)
    return SimulatedDevice()
