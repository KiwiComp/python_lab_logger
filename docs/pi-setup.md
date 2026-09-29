# Setting up a Raspberry Pi instrument

[`firmware/pi/instrument.py`](../firmware/pi/instrument.py) turns a Raspberry Pi into a
LabLogger instrument. It reports the Pi's CPU temperature, switches an alarm LED on
GPIO 17 and answers LabLogger on TCP port 5000, using the [protocol](protocol.md).


## Hardware

- A Raspberry Pi with Wi-Fi or Ethernet, and a power supply for your model
- A microSD card of at least 32 GB, and a card reader for your computer
- An LED and a resistor of about 220–330 Ω
- A breadboard and two female-to-male jumper wires


## Installing Raspberry Pi OS

1. **Write the SD card** with [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
   Choose your Pi model, *Raspberry Pi OS (64-bit)* and the SD card. On macOS, allow
   Imager to access the removable volume when asked.

2. **Customise the installation** before writing:

   - Hostname: `lablogger-pi`
   - A username and password of your choice
   - Your Wi-Fi network and password, and your country
   - Remote access: enable SSH with password authentication

3. **Start the Pi** with the card inserted, and wait about a minute for the first boot.


## Connecting over SSH

From your computer, with the username you chose:

```bash
ssh <user>@lablogger-pi.local
```

The first time, answer `yes` to trust the Pi's key. The password is not shown while you
type it. On macOS, the terminal app needs the Local Network permission, and a warning about
an invalid locale can be ignored; see [Troubleshooting](troubleshooting.md).

Update the system:

```bash
sudo apt update && sudo apt full-upgrade -y
```


## Getting the code

```bash
cd ~
git clone https://github.com/KiwiComp/python_lab_logger.git
cd python_lab_logger
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -c "import gpiozero; print('gpiozero OK')"
```

`--system-site-packages` lets the virtual environment use `gpiozero`, which comes with
Raspberry Pi OS. Activate the environment with `source .venv/bin/activate` in every new SSH
session. To get later changes, run `git pull` in the project directory.


## Wiring

Shut the Pi down and unplug it before wiring:

```bash
sudo shutdown now
```

- **LED:** GPIO 17 (physical pin 11) → resistor → the LED's long leg (anode). The short leg
  (cathode) goes to a GND pin, for example physical pin 9 or 39.

Run `pinout` on the Pi to see the pin layout of your model. Pin 1 is the pin with a square
solder pad on the underside of the board.

To check the wiring, start the Pi, activate the virtual environment and run `python`:

```python
from gpiozero import LED

led = LED(17)
led.on()  # the LED should light up
led.off()
```


## Running the instrument

```bash
python firmware/pi/instrument.py
```

It prints `Instrument listening on port 5000`. Check from your computer that it answers:

```bash
nc lablogger-pi.local 5000
```

Type `PING`, `READ`, `LED 1` and `LED 0`, one at a time. The Pi answers `OK PONG`, its CPU
temperature such as `OK VALUE=48.3`, `OK LED=1` and `OK LED=0`. Stop `nc` with Ctrl+C, and
the instrument with Ctrl+C on the Pi.


## Starting automatically with systemd

[`firmware/pi/lablogger-instrument.service`](../firmware/pi/lablogger-instrument.service)
runs the instrument as a systemd service, which starts it when the Pi boots and restarts
it if it crashes. The file assumes the user `kim` and the project in
`/home/kim/python_lab_logger`; change `User`, `WorkingDirectory` and `ExecStart` if your
username is different.

Install and start it:

```bash
sudo cp firmware/pi/lablogger-instrument.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now lablogger-instrument
```

Useful commands:

| Command | Does |
|---|---|
| `systemctl status lablogger-instrument` | Shows whether the service runs (press q to leave) |
| `journalctl -u lablogger-instrument -f` | Follows the service's log (Ctrl+C to leave) |
| `sudo systemctl restart lablogger-instrument` | Restarts it, for example after `git pull` |
| `sudo systemctl disable --now lablogger-instrument` | Stops it and no longer starts it at boot |

Do not start `instrument.py` by hand while the service runs, since both would use port
5000.


## Measuring

The default options are meant for the CPU temperature:

```bash
lablogger --host lablogger-pi.local --count 60 --db pi.db
```

To trigger the alarm, load the CPU in a second SSH session:

```bash
sudo apt install -y stress-ng
stress-ng --cpu 4 --timeout 60s
```

When the temperature goes above 60 °C, LabLogger marks it `ALARM` and the LED lights up.
If the Pi never gets that warm, use `--threshold 50`. With `lablogger-gui`, use the same
options except `--count`.


## Shutting down

```bash
sudo shutdown now
```

Wait until the green LED has stopped blinking before you unplug the power. Unplugging a
running Pi can damage the file system on the SD card.