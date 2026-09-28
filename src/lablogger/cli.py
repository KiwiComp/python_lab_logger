import argparse
import time

from lablogger.options import add_common_arguments, create_device
from lablogger.service import MeasurementService
from lablogger.storage import MeasurementRepository


def main() -> None:
    parser = argparse.ArgumentParser(description="LabLogger - measurement and logging")
    add_common_arguments(parser=parser)
    parser.add_argument(
        "--interval", type=float, default=1.0, help="Seconds between measurements"
    )
    parser.add_argument(
        "--count", type=int, default=10, help="Number of measurements to take"
    )
    args = parser.parse_args()

    device = create_device(args=args)
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
