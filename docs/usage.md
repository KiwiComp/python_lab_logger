# Using LabLogger

This guide assumes that LabLogger is installed as described in the
[README](../README.md#quick-start) and that the virtual environment is activated.


## Running with the simulated device

Without `--host`, LabLogger uses a simulated device whose temperature follows a slow wave
between about 35 and 65 °C. No hardware is needed.

```bash
lablogger --count 20
```

LabLogger takes one measurement per second, prints it and stores it in the database.
Values above the alarm threshold, 60 °C by default, are marked `ALARM`:

```text
10:20:57    59.1 °C
10:20:58    61.7 °C  ALARM
10:20:59    62.1 °C  ALARM
```

The run stops after `--count` measurements. Press Ctrl+C to stop earlier; the
measurements taken so far are kept.


## Running the GUI

```bash
lablogger-gui
```

Press **Start** to begin measuring and **Stop** to pause. The GUI takes one measurement per
second, shows the latest value, turns the status red while the value is above the
threshold, and adds each measurement to the table and the database. It keeps measuring
until you press Stop or close the window.

The GUI takes the same options as the command line, except `--interval` and `--count`.
With `--host`, it connects to the instrument when it starts, so start the instrument first.
If the connection is lost while measuring, measuring stops and an error dialog is shown.


## Running against the fake instrument

`tools/fake_instrument.py` is a local stand-in for a real instrument. It speaks the same
protocol and answers `READ` with a random raw value from 0 to 4095, like the ESP32.

In one terminal, start the fake instrument:

```bash
python tools/fake_instrument.py
```

In a second terminal, run LabLogger against it:

```bash
lablogger --host 127.0.0.1 --channel potentiometer --unit raw --threshold 3000 --count 20 --db fake.db
```

The fake instrument prints `LED on` and `LED off` when LabLogger switches the alarm LED.
Stop it with Ctrl+C. Use `127.0.0.1` rather than `localhost`, see
[Troubleshooting](troubleshooting.md).


## Running against a Raspberry Pi

Set up the Pi as described in [pi-setup.md](pi-setup.md). The default options are meant for
its CPU temperature, so only the address is needed:

```bash
lablogger --host lablogger-pi.local --count 60 --db pi.db
```


## Running against an ESP32

Set up the ESP32 as described in [esp32-setup.md](esp32-setup.md), then run LabLogger with
the board's IP address:

```bash
lablogger --host <ESP32 address> --channel potentiometer --unit raw --threshold 3000 --count 60 --db esp32.db
```


## Options

| Option | Default | Description |
|---|---|---|
| `--host` | (none) | Instrument address. Without it, the simulated device is used. |
| `--port` | `5000` | Instrument TCP port |
| `--db` | `lablogger.db` | SQLite database file. It is created if it does not exist. |
| `--threshold` | `60.0` | Alarm threshold. The alarm is active while the value is above it. |
| `--channel` | `cpu_temp` | Channel name stored with each value |
| `--unit` | `°C` | Unit stored with each value |
| `--interval` | `1.0` | Seconds between measurements (`lablogger` only) |
| `--count` | `10` | Number of measurements to take (`lablogger` only) |

The defaults are meant for a temperature. With a raw value from the ESP32 or the fake
instrument, set `--channel`, `--unit` and `--threshold` as in the examples above. Use a
separate `--db` file for each instrument, so that values with different units are not
mixed in the same database.


## Stored data

Each database file has two tables:

| Table | Columns | Content |
|---|---|---|
| `measurements` | `id`, `timestamp`, `channel`, `value`, `unit` | One row per measurement |
| `events` | `id`, `timestamp`, `kind`, `message` | One row per alarm change, with `kind` `ALARM_ON` or `ALARM_OFF` and the value in `message` |

Timestamps are stored in UTC as ISO 8601 text, for example
`2026-09-28T08:20:58.618007+00:00`. The command line and the GUI show them in local time.

To read the data from Python:

```python
from lablogger.storage import MeasurementRepository

repo = MeasurementRepository("lablogger.db")
for m in repo.latest(10):
    print(m.timestamp.astimezone(), m.channel, m.value, m.unit)
for timestamp, kind, message in repo.events():
    print(timestamp, kind, message)
repo.close()
```

Or with the `sqlite3` command-line tool on macOS and Linux:

```bash
sqlite3 lablogger.db "SELECT timestamp, channel, value, unit FROM measurements ORDER BY id DESC LIMIT 10;"
```