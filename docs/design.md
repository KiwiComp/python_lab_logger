# Design decisions

This document describes the main choices behind LabLogger and why they were made.


## An abstract device

`MeasurementService` does not know which device it talks to. It receives a `Device`, an
abstract base class with four methods: `connect`, `close`, `read_value` and `set_led`.
`SimulatedDevice` and `TcpDevice` implement it, and so does the fake device in the tests.

The device, the repository and the clock are passed to the service from outside
(dependency injection). This makes the service easy to test with a fake device and fixed
values, and adding a new kind of instrument, for example one connected over USB, only
requires a new `Device` class. `options.py` is the only place that decides which device
to create.


## Alarm on state changes

The service stores every measurement, but it only acts when the alarm state changes: it
sends `LED 1` and stores an `ALARM_ON` event when the value goes above the threshold, and
`LED 0` and `ALARM_OFF` when it is no longer above. While the state is unchanged, nothing
is sent. This avoids repeating commands to the instrument, and the event table becomes a
short record of when the alarm was active.

The alarm is active while the value is strictly above the threshold. There is no
hysteresis, so a value that hovers around the threshold can switch the alarm on and off
several times. A hysteresis band would avoid this, at the cost of one more setting.

When measuring is stopped while the alarm is active, the LED stays on, since no command is
sent to turn it off.


## A line-based text protocol

LabLogger and the instrument exchange short lines of ASCII text, such as `READ` and
`OK VALUE=2048`, described in [protocol.md](protocol.md). A text protocol is easy to
implement on a microcontroller, easy to test by hand with `nc`, and easy to read when
debugging. Each message ends with a newline, since TCP delivers a stream of bytes without
message boundaries.

Parsing is kept in `protocol.py`, separate from the network code, so that it can be tested
without a connection. `TcpDevice` checks the instrument before trusting it: it sends
`PING` right after connecting and requires `OK PONG`, and it checks that the instrument
confirms each LED command. All communication problems are raised as `DeviceError` or
`ProtocolError`, so the rest of the program only needs to handle LabLogger's own errors.


## Storage in SQLite with plain SQL

Measurements and events are stored in SQLite, which needs no server and keeps each
database in a single file. The queries are written in plain SQL rather than with an ORM,
since there are only a few of them. All values are passed as parameters (`?`) rather than
formatted into the SQL text, which prevents SQL injection.

`Measurement` is a frozen dataclass, so a measurement cannot be changed after it has been
created.


## Timestamps in UTC

All timestamps are stored in UTC, with the offset included, for example
`2026-09-28T08:20:58.618007+00:00`. Local time is ambiguous: when daylight saving time
ends, the same local hour occurs twice. Storing UTC keeps the records unambiguous, and the
command line and the GUI convert to local time only for display.


## Testable without hardware

The system can be developed and tested without an instrument:

- `SimulatedDevice` produces a temperature that follows a slow sine wave with noise. It
  accepts an optional seed, so the noise can be repeated when debugging, although the
  values also depend on when they are read.
- `tools/fake_instrument.py` speaks the real protocol on the local computer, so the network
  code can be tested end to end.
- The automated tests use a fake device with fixed values, so they are fully deterministic.

Parts that need a person or hardware, such as the GUI and the ESP32, are covered by the
[manual tests](manual-tests.md), and [requirements.md](requirements.md) links every
requirement to the tests that verify it.


## Shared options

`lablogger` and `lablogger-gui` define their shared command-line options in one place,
`options.py`, so that the two programs cannot get different defaults. The instrument
programs, on the other hand, share no code: the ESP32 firmware runs MicroPython on
separate hardware. What they share is the protocol, which is the contract between them and
LabLogger.