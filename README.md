# LabLogger

A measurement and control system in Python. A Raspberry Pi acts as an instrument
that reports its CPU temperature and drives an alarm LED over a simple TCP protocol,
while LabLogger reads, stores and displays the measurements.


## Project Structure

```
python_lab_logger/
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── docs/
│   ├── requirements.md
│   ├── protocol.md
│   └── manual-tests.md
├── firmware/
│   ├── pi_instrument.py
│   └── lablogger-instrument.service
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
└── tests/
    ├── test_protocol.py
    ├── test_storage.py
    └── test_service.py
```


## Design decisions

### Reproducible simulation
`SimulatedDevice` produces a temperature that follows a slow sine wave with
Gaussian noise, so the whole system can be developed and tested without hardware.
The noise comes from a random number generator that accepts an optional seed:

    device = SimulatedDevice(seed=42)

Two devices created with the same seed produce the same noise sequence.
This makes test runs and debugging sessions reproducible, which is essential
when results need to be verified and compared over time.


## Known limitations

- **No schema migrations.** The database schema is created with
  `CREATE TABLE IF NOT EXISTS`, so changes to the schema are not applied to an
  existing database file. Until versioned migrations are added, an existing
  `lablogger.db` must be deleted after a schema change, which discards its data.