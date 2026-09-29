# Manual tests

These tests cover what the automated tests do not: the commands, the GUI and the hardware.
Run them before merging changes to the code they cover, and record each run in the
[test log](#test-log). Requirements are listed in [requirements.md](requirements.md).

Run the tests from the project directory with the virtual environment activated. They use
the database file `test.db`; delete it when you are done.


## MT-01: Command line with the simulated device

Verifies: REQ-005

1. Run `lablogger --count 5 --db test.db`.

Expected: five lines about one second apart, each with a time and a value in °C. The
first value is close to 50 °C, and the values then rise slowly. The program then exits.


## MT-02: Command line with the fake instrument

Verifies: REQ-001, REQ-003, REQ-004, REQ-007

1. In one terminal, run `python tools/fake_instrument.py`.
2. In a second terminal, run:

   ```bash
   lablogger --host 127.0.0.1 --channel potentiometer --unit raw --threshold 3000 --count 20 --db test.db
   ```

3. Stop the fake instrument with Ctrl+C.

Expected:

- Twenty lines with values between 0 and 4095 and the unit `raw`.
- Exactly the lines with a value above 3000 end with `ALARM`.
- The fake instrument prints `LED on` each time the alarm turns on and `LED off` each time
  it turns off.


## MT-03: No connection and no response

Verifies: REQ-006

1. Make sure the fake instrument is not running, and run:

   ```bash
   lablogger --host 127.0.0.1 --count 1 --db test.db
   ```

2. In one terminal, start the fake instrument with `python tools/fake_instrument.py`.
3. In a second terminal, start a run that keeps the connection open for 30 seconds:

   ```bash
   lablogger --host 127.0.0.1 --channel potentiometer --unit raw --threshold 3000 --count 30 --db test.db
   ```

4. While it runs, run this in a third terminal:

   ```bash
   lablogger --host 127.0.0.1 --count 1 --db test.db
   ```

5. When the run in step 3 is done, stop the fake instrument with Ctrl+C, so that the next
   test starts without it.

Expected:

- Step 1 stops with an error whose last line ends with
  `Could not connect to 127.0.0.1:5000: [Errno 61] Connection refused`.
- Step 4 stops after about one second with an error whose last line ends with
  `Timeout: no response to 'PING'`, since the fake instrument serves one connection at a
  time.
- The run in step 3 is not affected and takes all 30 measurements.


## MT-04: GUI with the simulated device

Verifies: REQ-005, REQ-008

1. Run `lablogger-gui --db test.db`.
2. Before pressing anything, check the window.
3. Press **Start** and wait a few seconds.
4. Press **Stop** and wait a few seconds.
5. Press **Start** again, wait a few seconds, and close the window.

Expected:

- In step 2, the value shows `-` and the status `Stopped`. Start is enabled, Stop is
  disabled, and the table is empty.
- In step 3, Start is disabled and Stop is enabled. About once per second the value is
  updated and a new row with time, value and unit is added to the table.
- In step 4, the status is `Stopped`, no new rows are added, and Start is enabled again.
- In step 5, new rows are added again, and closing the window ends the program.


## MT-05: GUI alarm

Verifies: REQ-003, REQ-004, REQ-008

The simulated value starts at about 50 °C when the program starts, goes above the default
threshold of 60 °C after about 7 seconds, and falls below it again after about 24 seconds.

1. Run `lablogger-gui --db test.db` and press **Start** right away.
2. Keep measuring for 30 seconds, then close the window.

Expected:

- While the value is 60 °C or less, the status is `Measuring - normal`.
- When the value goes above 60 °C, the status changes to `ALARM - value above threshold`
  in red.
- When the value falls back to 60 °C or less, the status returns to `Measuring - normal`.
- Close to the threshold, the noise can make the status switch back and forth a couple of
  times. This is expected, since the alarm has no hysteresis.


## MT-06: GUI loses the connection

Verifies: REQ-006, REQ-007, REQ-008

1. In one terminal, run `python tools/fake_instrument.py`.
2. In a second terminal, run:

   ```bash
   lablogger-gui --host 127.0.0.1 --channel potentiometer --unit raw --threshold 3000 --db test.db
   ```

3. Press **Start** and wait a few seconds.
4. Stop the fake instrument with Ctrl+C.
5. Close the error dialog, then close the window.

Expected:

- In step 3, values between 0 and 4095 with the unit `raw` are shown and added to the
  table, and the status turns red when a value is above 3000.
- In step 4, measuring stops within a second and an error dialog is shown, for example
  `Connection closed by device`.
- In step 5, the status is `Stopped` and Start is enabled.


## MT-07: Command line with the ESP32 instrument

Verifies: REQ-001, REQ-003, REQ-004

Requires an ESP32 set up as in
[Setting up an ESP32 instrument](../README.md#setting-up-an-esp32-instrument), powered on
and connected to the same network as the computer.

1. Run:

   ```bash
   lablogger --host <ESP32 address> --channel potentiometer --unit raw --threshold 3000 --count 30 --db test.db
   ```

2. While it runs, turn the potentiometer slowly from one end to the other and back.

Expected:

- The values follow the potentiometer, from about 0 at one end to about 4095 at the other.
- When the value goes above 3000, the line is marked `ALARM` and the LED lights up.
- When the value falls back to 3000 or less, the LED turns off.


## MT-08: GUI with the ESP32 instrument

Verifies: REQ-003, REQ-004, REQ-007, REQ-008

Requires an ESP32 set up as in MT-07.

1. Run:

   ```bash
   lablogger-gui --host <ESP32 address> --channel potentiometer --unit raw --threshold 3000 --db test.db
   ```

2. Press **Start** and turn the potentiometer slowly from one end to the other and back.
3. Press **Stop** and close the window.

Expected:

- The value and the table follow the potentiometer, with the unit `raw`.
- When the value goes above 3000, the status turns red and the LED lights up.
- When the value falls back to 3000 or less, the status returns to `Measuring - normal`
  and the LED turns off.


## MT-09: Command line with the Raspberry Pi instrument

Verifies: REQ-001, REQ-003, REQ-004, REQ-007

Requires a Raspberry Pi set up as in [pi-setup.md](pi-setup.md), with the instrument
running and `stress-ng` installed (`sudo apt install -y stress-ng`).

1. Run the command below and note the highest temperature. Call it *T* and add 5:

  ```bash
  lablogger --host lablogger-pi.local --count 5 --db test.db
  ```

2. Run, with *T* + 5 as the threshold:

  ```bash
  lablogger --host lablogger-pi.local --threshold <T + 5> --count 240 --db test.db
  ```

3. About ten seconds into the run, load the Pi's CPU from an SSH session:

  ```bash
  stress-ng --cpu 4 --timeout 30s
  ```

Expected:

- Step 1 prints five temperatures in °C.
- In step 2, when the temperature goes above the threshold, the line is marked `ALARM`
  and the LED lights up.
- After the load ends and the temperature falls back to the threshold or below, the LED
  turns off.


## MT-10: GUI with the Raspberry Pi instrument

Verifies: REQ-003, REQ-004, REQ-007, REQ-008

Requires a Raspberry Pi set up as in MT-09.

1. Measure the idle temperature as in step 1 of MT-09, and call the highest value *T*.
2. Run, with *T* + 5 as the threshold:

  ```bash
  lablogger-gui --host lablogger-pi.local --threshold <T + 5> --db test.db
  ```

3. Press **Start**. About ten seconds later, load the Pi's CPU for 30 seconds from an SSH
   session:

  ```bash
   stress-ng --cpu 4 --timeout 30s
  ```

4. Keep measuring until the temperature has fallen back to the threshold or below, then
   press **Stop** and close the window.

Expected:

- The value and the table show the temperature in °C, about once per second.
- When the temperature goes above the threshold, the status turns red and the LED lights
  up.
- When it falls back to the threshold or below, the status returns to
  `Measuring - normal` and the LED turns off.


## MT-11: The Raspberry Pi instrument starts automatically

Verifies: REQ-009

Requires a Raspberry Pi set up as in [pi-setup.md](pi-setup.md), with the systemd service
installed and enabled.

1. Restart the Pi from an SSH session with `sudo reboot`.
2. Wait about a minute. Without logging in to the Pi, run on your computer:

  ```bash
   lablogger --host lablogger-pi.local --count 5 --db test.db
  ```

3. Log in over SSH and run `systemctl status lablogger-instrument`. Note the number after
   `Main PID`.
4. Simulate a crash by killing that process:

  ```bash
   sudo kill -9 <Main PID>
  ```

5. Wait a few seconds and run `systemctl status lablogger-instrument` again.
6. Run the command from step 2 again on your computer.

Expected:

- Step 2 prints five temperatures, without anyone having started the instrument by hand.
- In step 3, the service is `enabled` and `active (running)`.
- In step 5, the service is `active (running)` again, with a new `Main PID`, a start time
  a few seconds ago and `Scheduled restart job` in the log lines.
- Step 6 prints five temperatures.


## Test log

| Date | Test | Setup | Result | Notes |
|---|---|---|---|---|
| 2026-09-28 | MT-01 | Simulated device | Pass | |
| 2026-09-28 | MT-02 | Fake instrument | Pass | |
| 2026-09-28 | MT-03 | Fake instrument | Pass | |
| 2026-09-28 | MT-04 | Simulated device | Pass | |
| 2026-09-28 | MT-05 | Simulated device | Pass | |
| 2026-09-28 | MT-06 | Fake instrument | Pass | Dialog: Connection closed by device |
| 2026-09-28 | MT-07 | ESP32, MicroPython | Pass | |
| 2026-09-28 | MT-08 | ESP32, MicroPython | Pass | |
| 2026-09-29 | MT-09 | Raspberry Pi | Fail | Threshold 47, count 90 and stress timeout 40s. Alarm turned on, but the temperature did not fall below the threshold before the run ended. Test procedure too short; updated. |
| 2026-09-29 | MT-09 | Raspberry Pi | Pass | Threshold 49, count 240 and stress timeout 30s. |
| 2026-09-29 | MT-10 | Raspberry Pi | Pass | Threshold 51 |
| 2026-09-29 | MT-11 | Raspberry Pi, systemd | Pass | |