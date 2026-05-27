from __future__ import annotations
from python.f1fast.domain.driver_id import DriverId
from python.f1fast.domain.driver_pace_result import DriverQualyPace
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class TeamQualyPace:
    team: str
    drivers: list[DriverQualyPace]
    session_name: str
    year: int
    round_number: int
    pace: float
    delta_to_field_pct: float

    def to_dict(self) -> dict:
        return {
            "team": self.team,
            "driver": self.drivers,
            "session_name": self.session_name,
            "year": self.year,
            "round_number": self.round_number,
            "pace": round(self.pace, 4),
            "delta": round(self.delta, 4)
        }