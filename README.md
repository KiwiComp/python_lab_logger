# LabLogger

A measurement and control system in Python. An instrument (a Raspberry Pi or an ESP32)
reports measurements and drives an alarm LED over a simple TCP protocol, while LabLogger
reads, stores and displays the measurements.


## Getting started

### Requirements

- Python 3.11 or newer
- macOS, Linux or Windows

### Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/KiwiComp/python_lab_logger.git
cd python_lab_logger
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell), create and activate the virtual environment with:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell refuses to run the script, allow local scripts once with
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

Install the project in editable mode, including the GUI and development tools:

```bash
pip install -e ".[gui,dev]"
```

This installs the `lablogger` command. The virtual environment must be activated
in every new terminal before the command is available.

### Running with a simulated device

No hardware is needed. Without `--host`, LabLogger uses a simulated device:

```bash
lablogger --count 20
```

Run `lablogger --help` to see all options.

### Running against the fake instrument

`tools/fake_instrument.py` is a local stand-in for the real instrument. It speaks the same
TCP protocol, which makes it possible to test the network code without hardware.

In one terminal, start the fake instrument:

```bash
python tools/fake_instrument.py
```

In a second terminal, run LabLogger against it:

```bash
lablogger --host localhost --channel potentiometer --unit raw --threshold 3000 --count 20
```

### Running the tests

```bash
pytest -v
```


## Project structure

```
python_lab_logger/
├── .gitignore
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── docs/
│   ├── requirements.md
│   ├── protocol.md
│   └── manual-tests.md
├── firmware/
│   ├── pi/
│   │   ├── instrument.py
│   │   └── lablogger-instrument.service
│   └── esp32/
│       ├── main.py
│       └── wifi_config_example.py
├── src/lablogger/
│   ├── __init__.py
│   ├── errors.py
│   ├── models.py
│   ├── protocol.py
│   ├── storage.py
│   ├── service.py
│   ├── cli.py
│   ├── devices/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── simulated.py
│   │   └── tcp_device.py
│   └── gui/
│       ├── __init__.py
│       ├── main_window.py
│       └── app.py
├── tests/
│   ├── test_protocol.py
│   ├── test_storage.py
│   └── test_service.py
└── tools/
    └── fake_instrument.py
```


## Design decisions

### Reproducible simulation
`SimulatedDevice` produces a temperature that follows a slow sine wave with
Gaussian noise, so the whole system can be developed and tested without hardware.
The noise comes from a random number generator that accepts an optional seed:

```python
device = SimulatedDevice(seed=42)
```

Two devices created with the same seed produce the same noise sequence.
This makes test runs and debugging sessions reproducible, which is essential
when results need to be verified and compared over time.


## Known limitations

- **No schema migrations.** The database schema is created with
  `CREATE TABLE IF NOT EXISTS`, so changes to the schema are not applied to an
  existing database file. Until versioned migrations are added, an existing
  `lablogger.db` must be deleted after a schema change, which discards its data.