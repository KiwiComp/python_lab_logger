import argparse
import sys

from PySide6.QtWidgets import QApplication

from lablogger.gui.main_window import MainWindow
from lablogger.options import add_common_arguments, create_device
from lablogger.service import MeasurementService
from lablogger.storage import MeasurementRepository


def main() -> None:
    parser = argparse.ArgumentParser(description="LabLogger GUI")
    add_common_arguments(parser=parser)
    args = parser.parse_args()

    app = QApplication(sys.argv)
    device = create_device(args=args)
    repo = MeasurementRepository(db_path=args.db)
    try:
        with device:
            service = MeasurementService(
                device=device,
                repo=repo,
                channel=args.channel,
                unit=args.unit,
                alarm_threshold=args.threshold,
            )
            window = MainWindow(service=service)
            window.show()
            exit_code = app.exec()
    finally:
        repo.close()
    sys.exit(exit_code)
