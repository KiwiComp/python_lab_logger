from abc import ABC, abstractmethod

# ABC plus @abstractmethod corresponds to abstract class in Dart. 
# The contract for every device.
class Device(ABC):
    """Common interface for real and simulated devices."""

    @abstractmethod
    def connect(self) -> None: ... # ... means it doesn't return anything.

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def read_value(self) -> float: ...

    @abstractmethod
    def set_led(self, on: bool) -> None: ...

    # If used together with device in a with block, automatically run in beginning (enter) and end (exit).
    def __enter__(self) -> "Device":
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()