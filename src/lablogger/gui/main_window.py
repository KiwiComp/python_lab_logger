from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from lablogger.errors import LabLoggerError
from lablogger.service import MeasurementService


class MainWindow(QMainWindow):
    def __init__(self, service: MeasurementService):
        super().__init__()
        self._service = service
        self.setWindowTitle("LabLogger")

        # Widgets
        self.value_label = QLabel("-")
        self.value_label.setStyleSheet("font-size: 32px")
        self.status_label = QLabel("Stopped")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Time", "Value", "Unit"])

        # Layout
        buttons = QHBoxLayout()
        buttons.addWidget(self.start_button)
        buttons.addWidget(self.stop_button)
        layout = QVBoxLayout()
        layout.addWidget(self.value_label)
        layout.addWidget(self.status_label)
        layout.addLayout(buttons)
        layout.addWidget(self.table)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Timer and signals
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_tick)
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

    def start(self) -> None:
        self.timer.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Measuring")

    def stop(self) -> None:
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Stopped")
        self.status_label.setStyleSheet("")

    def on_tick(self) -> None:
        try:
            m = self._service.sample()
        except LabLoggerError as exc:
            self.stop()
            QMessageBox.critical(self, "Error", str(exc))
            return

        self.value_label.setText(f"{m.value:.1f} {m.unit}")
        if self._service.alarm_active:
            self.status_label.setText("ALARM - value above threshold")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.status_label.setText("Measuring - normal")
            self.status_label.setStyleSheet("")

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(
            row, 0, QTableWidgetItem(f"{m.timestamp.astimezone():%H:%M:%S}")
        )
        self.table.setItem(row, 1, QTableWidgetItem(f"{m.value:.1f}"))
        self.table.setItem(row, 2, QTableWidgetItem(m.unit))
        self.table.scrollToBottom()
