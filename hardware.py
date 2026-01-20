import time
from typing import Optional

import serial


class HardwareBridge:
    """Handles serial I/O with the microcontroller."""

    def __init__(self, port: str, baud: int = 9600, timeout: float = 1.0) -> None:
        self.ser = serial.Serial(port, baudrate=baud, timeout=timeout)

    def close(self) -> None:
        if self.ser and self.ser.is_open:
            self.ser.close()

    def wait_for_trigger(self, trigger_text: str = "TRIGGER", poll: float = 0.1) -> bool:
        """Block until the trigger text is received."""
        while True:
            line = self.read_line()
            if line and line.strip().upper() == trigger_text.upper():
                return True
            time.sleep(poll)

    def read_line(self) -> Optional[str]:
        try:
            data = self.ser.readline().decode(errors="ignore")
            return data.strip() if data else None
        except Exception:
            return None

    def send_command(self, command: str) -> None:
        if not command.endswith("\n"):
            command += "\n"
        self.ser.write(command.encode())

    def open_servo(self) -> None:
        self.send_command("OPEN")

    def close_servo(self) -> None:
        self.send_command("CLOSE")

