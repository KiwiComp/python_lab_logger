# LabLogger protocol

Communication between LabLogger and the instrument uses plain ASCII text over TCP (port 5000).
Each message is one line terminated by a newline (`\n`). LabLogger sends a command and
waits for exactly one response line.

## Commands

| LabLogger sends   | Instrument replies        | Description                         |
|-------------------|---------------------------|-------------------------------------|
| `PING`            | `OK PONG`                 | Connection check                    |
| `READ`            | `OK VALUE=48.3`           | Current CPU temperature in °C       |
| `LED 1` / `LED 0` | `OK LED=1` / `OK LED=0`   | Turn the alarm LED on or off        |
| unknown command   | `ERR UNKNOWN_COMMAND`     | The command was not recognized      |

## Response format

- `OK <payload>` – the command succeeded
- `ERR <reason>` – the instrument reports an error
- Any other response is treated as a protocol error by LabLogger