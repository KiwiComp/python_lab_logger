

## Architecture Tree
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