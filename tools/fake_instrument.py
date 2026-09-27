"""Local stand-in for the instrument, for testing TcpDevice without hardware."""

import random
import socketserver

PORT = 5000


def handle_command(cmd: str) -> str:
    if cmd == "PING":
        return "OK PONG"
    if cmd == "READ":
        return f"OK VALUE={random.randint(0, 4095)}"
    if cmd == "LED 1":
        print("LED on")
        return "OK LED=1"
    if cmd == "LED 0":
        print("LED off")
        return "OK LED=0"
    return "ERR UNKNOWN_COMMAND"


class Handler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        for raw in self.rfile:
            reply = handle_command(cmd=raw.decode("ascii", errors="replace").strip())
            self.wfile.write((reply + "\n").encode("ascii"))


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as server:
        print(f"Fake instrument listening on port {PORT}")
        server.serve_forever()

# Run --> python tools/fake_instrument.py
