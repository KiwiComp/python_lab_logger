# LabLogger requirements

These are the requirements for LabLogger and the tests that verify each of them. The link
goes both ways: the table below lists the tests for each requirement, and each test names
the requirements it verifies, in its docstring (for example `"""Verifies REQ-002."""`) or,
for the manual tests in [manual-tests.md](manual-tests.md), on its *Verifies* line.

Requirements that are hard to test automatically, such as those for the GUI and the
hardware, are covered by manual tests instead. Two automated tests check details rather
than a requirement, and therefore have no requirement ID:
`tests/test_options.py::test_common_defaults` and
`tests/test_storage.py::test_latest_respects_limit_and_order`.

| ID | Requirement | Verified by |
|---|---|---|
| REQ-001 | LabLogger shall read measured values from an instrument over the TCP protocol described in [protocol.md](protocol.md). | `tests/test_protocol.py::test_parse_response_ok`, `tests/test_protocol.py::test_parse_value`, `tests/test_options.py::test_create_device_with_host_is_tcp`, MT-02, MT-07 |
| REQ-002 | Every measurement shall be stored in an SQLite database with its timestamp, channel name, value and unit. | `tests/test_storage.py::test_add_and_read_back` |
| REQ-003 | When a measured value goes above the alarm threshold, LabLogger shall turn on the instrument's alarm LED and store an `ALARM_ON` event. While the value stays above the threshold, LabLogger shall not send the LED command or store the event again. | `tests/test_service.py::test_alarm_turns_led_on_then_off`, MT-02, MT-05, MT-07, MT-08 |
| REQ-004 | When the value is no longer above the threshold, LabLogger shall turn off the alarm LED and store an `ALARM_OFF` event. | `tests/test_service.py::test_alarm_turns_led_on_then_off`, MT-02, MT-05, MT-07, MT-08 |
| REQ-005 | LabLogger shall be usable without hardware, with a simulated device. | `tests/test_options.py::test_create_device_without_host_is_simulated`, MT-01, MT-04 |
| REQ-006 | LabLogger shall report communication problems as errors: no connection, no response, a response that does not follow the protocol, and an error reported by the instrument. | `tests/test_protocol.py::test_parse_response_device_error`, `tests/test_protocol.py::test_parse_response_garbage`, `tests/test_protocol.py::test_parse_value_invalid_number`, MT-03, MT-06 |
| REQ-007 | The instrument address and port, the database file, the alarm threshold, the channel name and the unit shall be configurable from the command line, both for `lablogger` and for `lablogger-gui`. | `tests/test_options.py::test_common_arguments_can_be_set`, MT-02, MT-06, MT-08 |
| REQ-008 | A desktop GUI shall show the latest value, the alarm status and a table of the measurements, and let the user start and stop measuring. | MT-04, MT-05, MT-06, MT-08 |