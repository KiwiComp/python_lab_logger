# LabLogger protocol

Communication between LabLogger and the instrument uses plain ASCII text over TCP (port 5000).
Each message is one line terminated by a newline (`\n`). Commands are case-sensitive.
LabLogger sends a command and waits for exactly one response line.

LabLogger keeps one connection open for the whole session. Right after connecting it sends
`PING`, and it closes the connection and reports an error unless the instrument answers
`OK PONG`. It waits at most one second for each response. For `LED 1` and `LED 0`,
LabLogger checks that the reply confirms the requested state and reports an error
otherwise.

The instruments serve one connection at a time. A second connection is accepted by the
operating system but gets no response until the first one is closed.

## Commands

| LabLogger sends | Instrument replies | Description |
|---|---|---|
| `PING` | `OK PONG` | Connection check |
| `READ` | `OK VALUE=2048` | Current measured value, see below |
| `LED 1` / `LED 0` | `OK LED=1` / `OK LED=0` | Turn the alarm LED on or off |
| unknown command | `ERR UNKNOWN_COMMAND` | The command was not recognized |

## Measured values

The value after `VALUE=` is a number, with or without decimals. What it means depends on
the instrument:

| Instrument | Value | LabLogger options to use |
|---|---|---|
| ESP32 (`firmware/esp32/main.py`) | Raw 12-bit ADC reading of GPIO 34: an integer from 0 (0 V) to 4095 (about 3.3 V) | `--channel potentiometer --unit raw --threshold 3000` |
| Fake instrument (`tools/fake_instrument.py`) | A random integer from 0 to 4095, like the ESP32 | Same as for the ESP32 |
| Raspberry Pi (`firmware/pi/instrument.py`) | CPU temperature in °C, for example `48.3` | The defaults (`cpu_temp`, `°C`, threshold 60) |

## Response format

- `OK <payload>` – the command succeeded
- `ERR <reason>` – the instrument reports an error
- Any other response is treated as a protocol error by LabLogger