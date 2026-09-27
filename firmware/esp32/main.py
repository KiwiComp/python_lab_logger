"""LabLogger instrument firmware for ESP32 (MicroPython)."""

import socket
import time

import network
import wifi_config
from machine import ADC, Pin

PORT = 5000
led = Pin(23, Pin.OUT)
adc = ADC(Pin(34), atten=ADC.ATTN_11DB)  # measure the full 0-3.3 V range


def connect_wifi() -> None:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(wifi_config.WIFI_SSID, wifi_config.WIFI_PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            time.sleep(0.5)
    if not wlan.isconnected():
        raise RuntimeError("Could not connect to Wi-Fi")
    print("Connected, IP:", wlan.ifconfig()[0])


def handle_command(cmd: str) -> str:
    if cmd == "PING":
        return "OK PONG"
    if cmd == "READ":
        return f"OK VALUE={adc.read()}"
    if cmd == "LED 1":
        led.on()
        return "OK LED=1"
    if cmd == "LED 0":
        led.off()
        return "OK LED=0"
    return "ERR UNKNOWN_COMMAND"


def serve() -> None:
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORT))
    server.listen(1)
    print("Instrument listening on port", PORT)
    while True:
        client, _ = server.accept()
        stream = client.makefile("rwb")
        try:
            while True:
                raw = stream.readline()
                if not raw:
                    break
                reply = handle_command(raw.decode().strip())
                stream.write((reply + "\n").encode())
        finally:
            client.close()


connect_wifi()
serve()
