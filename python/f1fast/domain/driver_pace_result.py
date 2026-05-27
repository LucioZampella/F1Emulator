from __future__ import annotations
from dataclasses import dataclass, asdict
from python.f1fast.domain.driver_id import DriverId


@dataclass(frozen=True)
class SessionRacePaceDiff:
    driver1: DriverId
    driver2: DriverId
    team: str
    session_name: str
    year: int
    round_number: int
    avg_driver1_seconds: float
    avg_driver2_seconds: float
    delta_pct: float
    faster_driver: DriverId
    slower_driver: DriverId

    def to_dict(self) -> dict:
        return {
            "driver1": str(self.driver1),
            "driver2": str(self.driver2),
            "team": self.team,
            "session_name": self.session_name,
            "year": self.year,
            "round_number": self.round_number,
            "avg_driver1_seconds": round(self.avg_driver1_seconds, 4),
            "avg_driver2_seconds": round(self.avg_driver2_seconds, 4),
            "delta_pct": round(self.delta_pct, 4),
            "faster_driver": str(self.faster_driver),
            "slower_driver": str(self.slower_driver),
        }


@dataclass(frozen=True)
class SeasonRacePaceDiff:
    driver1: DriverId
    driver2: DriverId
    team: str
    year: int
    races_counted: int
    avg_delta_pct: float
    faster_driver: DriverId
    slower_driver: DriverId

    def to_dict(self) -> dict:
        return {
            "driver1": str(self.driver1),
            "driver2": str(self.driver2),
            "team": self.team,
            "year": self.year,
            "races_counted": self.races_counted,
            "avg_delta_pct": round(self.avg_delta_pct, 4),
            "faster_driver": str(self.faster_driver),
            "slower_driver": str(self.slower_driver),
        }


@dataclass(frozen=True)
class CareerRacePaceDiff:
    driver1: DriverId
    driver2: DriverId
    years_analyzed: tuple[int, ...]
    total_races: int
    avg_delta_pct: float
    faster_driver: DriverId
    slower_driver: DriverId

    def to_dict(self) -> dict:
        return {
            "driver1": str(self.driver1),
            "driver2": str(self.driver2),
            "years_analyzed": list(self.years_analyzed),
            "total_races": self.total_races,
            "avg_delta_pct": round(self.avg_delta_pct, 4),
            "faster_driver": str(self.faster_driver),
            "slower_driver": str(self.slower_driver),
        }

@dataclass
class DriverRacePace:
    driver: DriverId
    team: str
    session_name: str
    year: int
    round_number: int
    avg_seconds: float
    delta_to_field_pct: float

    def to_dict(self) -> dict:
        return {
            "driver": str(self.driver),
            "team": self.team,
            "session_name": self.session_name,
            "year": self.year,
            "round_number": self.round_number,
            "avg_seconds": round(self.avg_seconds, 4),
            "delta_to_field_pct": round(self.delta_to_field_pct, 4)
        }

@dataclass(frozen=True)
class SeasonDriverPace:
    driver: DriverId
    team: str
    year: int
    races_counted: int
    avg_delta_to_field_pct: float

    def to_dict(self) -> dict:
        return {
            "driver": str(self.driver),
            "team": self.team,
            "year": self.year,
            "races_counted": self.races_counted,
            "avg_delta_to_field_pct": round(self.avg_delta_to_field_pct, 4),
        }

@dataclass(frozen=True)
class SessionQualyPaceDiff:
    driver1: DriverId
    driver2: DriverId
    team: str
    session_name: str
    year: int
    round_number: int
    driver1_qualy: float
    driver2_qualy: float
    delta_pct: float
    faster_driver: DriverId
    slower_driver: DriverId

    def to_dict(self) -> dict:
        return {
            "driver1": str(self.driver1),
            "driver2": str(self.driver2),
            "team": self.team,
            "session_name": self.session_name,
            "year": self.year,
            "round_number": self.round_number,
            "driver1_qualy": round(self.driver1_qualy, 4),
            "driver2_qualy": round(self.driver2_qualy, 4),
            "delta_pct": round(self.delta_pct, 4),
            "faster_driver": str(self.faster_driver),
            "slower_driver": str(self.slower_driver),
        }

@dataclass(frozen=True)
class DriverQualyPace:
    driver: DriverId
    team: str
    session_name: str
    year: int
    round_number: int
    qualy_time: float
    delta_to_field_pct: float

    def to_dict(self) -> dict:
        return {
            "driver": str(self.driver),
            "team": self.team,
            "session_name": self.session_name,
            "year": self.year,
            "round_number": self.round_number,
            "qualy_time": round(self.qualy_time, 4),
            "delta_to_field_pct": round(self.delta_to_field_pct, 4)
        }


@dataclass(frozen=True)
class SeasonQualyPaceDiff:
    driver1: DriverId
    driver2: DriverId
    team: str
    year: int
    races_counted: int
    avg_delta_pct: float
    faster_driver: DriverId
    slower_driver: DriverId

    def to_dict(self) -> dict:
        return {
            "driver1": str(self.driver1),
            "driver2": str(self.driver2),
            "team": self.team,
            "year": self.year,
            "races_counted": self.races_counted,
            "avg_delta_pct": round(self.avg_delta_pct, 4),
            "faster_driver": str(self.faster_driver),
            "slower_driver": str(self.slower_driver),
        }


@dataclass(frozen=True)
class SeasonDriverQualyPace:
    driver: DriverId
    team: str
    year: int
    races_counted: int
    avg_delta_to_field_pct: float

    def to_dict(self) -> dict:
        return {
            "driver": str(self.driver),
            "team": self.team,
            "year": self.year,
            "races_counted": self.races_counted,
            "avg_delta_to_field_pct": round(self.avg_delta_to_field_pct, 4),
        }
