from __future__ import annotations
from python.f1fast.domain.driver_id import DriverId
from python.f1fast.domain.driver_pace_result import DriverQualyPace
from dataclasses import dataclass, asdict


class TeamRacePace:
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
            "delta_to_field_pct": round(self.delta_to_field_pct, 4)
        }

@dataclass(frozen=True)
class SeasonTeamRacePace:
    team: str
    year: int
    races_counted: int
    avg_delta_to_field_pct: float

    def to_dict(self) -> dict:
        return {
            "team": self.team,
            "year": self.year,
            "races_counted": self.races_counted,
            "avg_delta_to_field_pct": round(self.avg_delta_to_field_pct, 4),
        }

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
            "delta_to_field_pct": round(self.delta_to_field_pct, 4)
        }

@dataclass(frozen=True)
class SeasonTeamQualyPace:
    team: str
    year: int
    races_counted: int
    avg_delta_to_field_pct: float

    def to_dict(self) -> dict:
        return {
            "team": self.team,
            "year": self.year,
            "races_counted": self.races_counted,
            "avg_delta_to_field_pct": round(self.avg_delta_to_field_pct, 4),
        }