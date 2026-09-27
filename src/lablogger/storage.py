import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from lablogger.models import Measurement

SCHEMA = """
CREATE TABLE IF NOT EXISTS measurements (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    channel   TEXT NOT NULL,
    value     REAL NOT NULL,
    unit      TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    kind      TEXT NOT NULL,
    message   TEXT NOT NULL
);
"""


class MeasurementRepository:
    # Consider making it safer by removing default memory string
    def __init__(self, db_path: str | Path = ":memory:"):
        self._conn = sqlite3.connect(db_path)
        self._conn.executescript(SCHEMA)

    def add(self, m: Measurement) -> int:
        with self._conn:  # transaction: commit on success, rollback on error
            cur = self._conn.execute(
                "INSERT INTO measurements (timestamp, channel, value, unit) "
                "VALUES (?, ?, ?, ?)",
                (m.timestamp.isoformat(), m.channel, m.value, m.unit),
            )
        row_id = cur.lastrowid
        if row_id is None:
            raise RuntimeError("Insert did not return a row id")
        return row_id

    def add_event(self, kind: str, message: str) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO events (timestamp, kind, message) VALUES (?, ?, ?)",
                (datetime.now(UTC).isoformat(), kind, message),
            )

    def latest(self, limit: int = 100) -> list[Measurement]:
        rows = self._conn.execute(
            "SELECT timestamp, channel, value, unit FROM measurements "
            "ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [
            Measurement(
                timestamp=datetime.fromisoformat(ts),
                channel=ch,
                value=val,
                unit=unit,
            )
            for ts, ch, val, unit in reversed(rows)
        ]

    def events(self) -> list[tuple[str, str, str]]:
        return self._conn.execute(
            "SELECT timestamp, kind, message FROM events ORDER BY id"
        ).fetchall()

    def close(self) -> None:
        self._conn.close()
