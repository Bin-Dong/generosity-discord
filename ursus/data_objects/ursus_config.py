from dataclasses import dataclass

from .interval import Interval

@dataclass
class UrsusConfig:
    time_format: str
    time_zone: str
    intervals: list[Interval]
    voice_channel_id: int