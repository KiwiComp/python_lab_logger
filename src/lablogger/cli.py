import argparse
import time

from lablogger.devices.simulated import SimulatedDevice
from lablogger.devices.tcp_device import TcpDevice
from lablogger.service import MeasurementService
from lablogger.storage import MeasurementRepository


def main() -> None:
    parser = argparse.ArgumentParser(description="LabLogger - measurement and logging")
    parser.add_argument(
        "--host",
        help="Instrument address, e.g. lablogger-pi.local. Omit for simulation.",
    )
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--db", default="lablogger.db")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--threshold", type=float, default=60.0)
    parser.add_argument("--channel", default="cpu_temp")
    parser.add_argument("--unit", default="°C")
    args = parser.parse_args()

    device = TcpDevice(args.host, args.port) if args.host else SimulatedDevice()
    repo = MeasurementRepository(args.db)
    try:
        with device:
            service = MeasurementService(
                device,
                repo,
                channel=args.channel,
                unit=args.unit,
                alarm_threshold=args.threshold,
            )
            for _ in range(args.count):
                m = service.sample()
                flag = "  ALARM" if service.alarm_active else ""
                print(
                    f"{m.timestamp.astimezone():%H:%M:%S}  {m.value:6.1f} {m.unit}{flag}"
                )
                time.sleep(args.interval)
    finally:
        repo.close()
