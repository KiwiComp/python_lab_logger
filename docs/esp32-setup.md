# Setting up an ESP32 instrument

[`firmware/esp32/main.py`](../firmware/esp32/main.py) turns an ESP32 into a LabLogger
instrument. It connects to your Wi-Fi network, reads an analog voltage, switches an alarm
LED and answers LabLogger on TCP port 5000, using the [protocol](protocol.md).


## Hardware

- An ESP32 development board and a USB data cable (a charging-only cable does not work)
- An LED and a resistor of about 220–330 Ω
- A potentiometer, for example 10 kΩ
- A breadboard and jumper wires
- A 2.4 GHz Wi-Fi network (the ESP32 cannot use 5 GHz networks)


## Wiring

Unplug the USB cable while wiring.

- **LED:** GPIO 23 → resistor → the LED's long leg (anode). The short leg (cathode) goes
  to GND.
- **Potentiometer:** the outer pins go to 3V3 and GND, and the middle pin to GPIO 34.

Never connect GPIO 34 to 5V or VIN; it takes at most 3.3 V. The pin labels on the board
vary, for example `23`, `D23` or `IO23`.


## Installing the firmware

1. **Install MicroPython** on the board. Follow the instructions for your board at
   [micropython.org/download](https://micropython.org/download/?port=esp32); most boards
   use the [generic ESP32 firmware](https://micropython.org/download/ESP32_GENERIC/).

2. **Install `mpremote`**, the tool that copies files to the board, in the virtual
   environment:

    ```bash
    pip install mpremote
    ```

3. **Check the wiring** from the board's interactive prompt. Open it with `mpremote repl`,
   press Ctrl+C to get the `>>>` prompt, and run:

    ```python
    from machine import ADC, Pin

    Pin(23, Pin.OUT).on()  # the LED should light up
    ADC(Pin(34), atten=ADC.ATTN_11DB).read()  # turn the potentiometer and repeat
    ```

   The value should change between about 0 and 4095. Leave the prompt with Ctrl+X.

4. **Create your Wi-Fi settings** from the template, then open
   `firmware/esp32/wifi_config.py` and fill in your network name and password:

    ```bash
    cp firmware/esp32/wifi_config_example.py firmware/esp32/wifi_config.py
    ```

   `wifi_config.py` is ignored by Git, so your password is never committed.

5. **Copy both files** to the board and restart it:

    ```bash
    mpremote cp firmware/esp32/wifi_config.py :wifi_config.py
    mpremote cp firmware/esp32/main.py :main.py
    mpremote reset
    ```

   The board runs `main.py` automatically every time it starts.

6. **Find the board's IP address.** Open `mpremote repl`, press Ctrl+C to stop the
   firmware, then Ctrl+D to restart it. After a few seconds it prints:

   ```text
   Connected, IP: 192.168.x.x
   Instrument listening on port 5000
   ```

   Leave the prompt with Ctrl+X; the firmware keeps running. You can also find the address
   in your router's list of connected devices.


## Checking the instrument

Before running LabLogger, check that the board answers from your computer:

```bash
nc <ESP32 address> 5000
```

Type the commands below one at a time, in capital letters:

```text
PING
READ
LED 1
LED 0
```

The board answers `OK PONG`, `OK VALUE=...`, `OK LED=1` and `OK LED=0`, and the LED
turns on and off. Stop `nc` with Ctrl+C, since the board serves one connection at a time.

If `nc` fails, see [Troubleshooting](troubleshooting.md).


## Measuring

```bash
lablogger --host <ESP32 address> --channel potentiometer --unit raw --threshold 3000 --count 60 --db esp32.db
```

Turn the potentiometer: when the value goes above 3000, LabLogger marks it `ALARM` and the
LED lights up. When the value falls back, the LED turns off. With `lablogger-gui`, use the
same options except `--count`.

The IP address can change when the board restarts. To keep it fixed, reserve it for the
board in your router's settings (often called DHCP reservation).