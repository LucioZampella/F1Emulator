from dataclasses import dataclass


@dataclass
class RacePaceDiff:
    driver1_number: str
    driver2_number: str
    team: str
    session: str
    avg_driver1: float
    avg_driver2: float
    delta: float
    faster_driver_number: int
    slower_driver_number: int