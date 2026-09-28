# Changelog

All notable changes to LabLogger are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

LabLogger has not had a release yet, so all changes are listed under Unreleased.

## [Unreleased]

### Added

- Documentation: ESP32 setup, the GUI, command-line options, architecture, alarm logic,
  stored data and troubleshooting in the README, plus requirements, manual tests and this
  changelog.
- MIT license.
- Desktop GUI, started with `lablogger-gui`, with start and stop, the latest value, the
  alarm status and a table of measurements. It shares its command-line options with
  `lablogger`.
- `TcpDevice` for talking to an instrument over TCP, and a fake instrument
  (`tools/fake_instrument.py`) for testing without hardware.
- ESP32 instrument firmware (MicroPython), and the `--channel` and `--unit` options.
- Measurement service with alarm logic, and the `lablogger` command.
- SQLite storage of measurements and alarm events.
- `Measurement` model, device interface and simulated device.
- Protocol description and parsing of instrument responses.

### Fixed

- The protocol description said that `READ` returns the CPU temperature, which only applies
  to the planned Raspberry Pi instrument. It now describes the value for each instrument.
