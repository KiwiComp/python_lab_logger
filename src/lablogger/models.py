from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Measurement:
    timestamp: datetime
    channel: str
    value: float
    unit: str