# Troubleshooting


## Commands are not found

**`lablogger: command not found`** (on Windows: *not recognized*), or the same for
`mpremote`. The virtual environment is not active in this terminal. Activate it with
`source .venv/bin/activate`, or `.venv\Scripts\Activate.ps1` on Windows. Every new
terminal needs it.


## Connection errors

When LabLogger cannot talk to the instrument, it stops with a traceback. The last line
starts with `lablogger.errors.DeviceError:` or `lablogger.errors.ProtocolError:`, followed
by one of these messages. In the GUI, errors that happen while measuring are shown in an
error dialog instead.

| Message | What it means |
|---|---|
| `Could not connect to <address>:5000: [Errno 61] Connection refused` | Nothing listens on that address and port. Start the instrument or the fake instrument, and check `--host` and `--port`. The error number differs between operating systems. |
| `Could not connect to <address>:5000: timed out` | The address cannot be reached: the IP address is wrong, the instrument is off, or it is on another network. |
| `Could not connect to <address>:5000: [Errno 65] No route to host` | On macOS, usually a missing Local Network permission, see below. |
| `Timeout: no response to 'PING'` | Something accepted the connection but does not answer. The instrument may be busy with another connection, since it serves one at a time. |
| `Unexpected response: ...` | A program that is not a LabLogger instrument answered on the port. |
| `Connection closed by device` | The instrument closed the connection, for example because it was stopped or restarted. Start LabLogger again. |


## macOS: No route to host

Recent versions of macOS require permission for apps that talk to other devices on the
local network. Without it, connections to the ESP32 fail with `No route to host`, even
though the network works.

Open System Settings → Privacy & Security → Local Network, turn on the app you run the
commands from (for example Visual Studio Code or Terminal), and restart that app.


## macOS: port 5000 is taken

On macOS 12 and later, the AirPlay Receiver listens on port 5000 by default. The fake
instrument can then fail with `Address already in use`, or LabLogger may reach AirPlay
and report a timeout or an unexpected response. Check what is listening with:

```bash
lsof -nP -iTCP:5000 -sTCP:LISTEN
```

Turn off AirPlay Receiver in System Settings → General → AirDrop & Handoff.


## localhost versus 127.0.0.1

The fake instrument only listens on the IPv4 address `127.0.0.1`, while `localhost` is
often tried as the IPv6 address `::1` first. If another program answers on `::1`,
LabLogger talks to that program instead. Use `--host 127.0.0.1` for the fake instrument.


## ESP32

**The board is not found over USB.** Check that the cable carries data; many USB cables
only charge. List the serial ports with `ls /dev/cu.*` on macOS; the board shows up as
something like `/dev/cu.usbserial-...`. Some boards need a USB driver from the maker of
their USB chip.

**`mpremote` cannot open the port.** Only one program at a time can use the board's
serial port. Close any other `mpremote repl` with Ctrl+X, and try again.

**The prompt shows no `>>>`.** The firmware is running and keeps the board busy. Press
Ctrl+C to stop it and get the prompt; Ctrl+D restarts it.

**`Could not connect to Wi-Fi`.** Check the network name and password in
`wifi_config.py`, and that the network uses 2.4 GHz. Copy the file to the board again
after changing it.

**`nc` or LabLogger cannot reach the board.** Check that the computer and the board are on
the same network, and that the network does not isolate its devices from each other,
which guest networks often do.