"""Instrument program for Raspberry Pi. Answers the LabLogger protocol over TCP."""

import socketserver
from pathlib import Path

from gpiozero import LED

TEMP_FILE = Path("/sys/class/thermal/thermal_zone0/temp")
PORT = 5000
led = LED(17)


def handle_command(cmd: str) -> str:
    if cmd == "PING":
        return "OK PONG"
    if cmd == "READ":
        millidegrees = int(TEMP_FILE.read_text())
        return f"OK VALUE={millidegrees / 1000:.1f}"
    if cmd == "LED 1":
        led.on()
        return "OK LED=1"
    if cmd == "LED 0":
        led.off()
        return "OK LED=0"
    return "ERR UNKNOWN_COMMAND"


class Handler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        # self.rfile is the connection as a file – each iteration yields one line
        for raw in self.rfile:
            reply = handle_command(raw.decode("ascii", errors="replace").strip())
            self.wfile.write((reply + "\n").encode("ascii"))


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as server:
        print(f"Instrument listening on port {PORT}")
        server.serve_forever()
