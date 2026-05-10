import pandas as pd

from python.f1fast.main.filters.LapFilter import LapFilter
from python.f1fast.main.validators.LapsValidator import LapsValidator as lv

class DriversPaceComparator:

    def __init__(self, lap_filter: LapFilter):
        self.lap_filter = lap_filter

    def compare(self, laps_d1: pd.DataFrame, laps_d2: pd.DataFrame) -> tuple[float, float] | None:
        laps_d1, laps_d2 = self.lap_filter.filter_comparable_stints(laps_d1, laps_d2)

        if laps_d1.empty or laps_d2.empty:
            return None

        laps_d1, laps_d2 = self.lap_filter.adjust_fuel_consumption(laps_d1, laps_d2)

        if laps_d1.empty or laps_d2.empty:
            return None

        if len(laps_d1) < 10 or len(laps_d2) < 10:
            return None

        ratio = max(len(laps_d1), len(laps_d2)) / min(len(laps_d1), len(laps_d2))
        if ratio > 2.5:
            return None

        avg1 = laps_d1["LapTime"].mean().total_seconds()
        avg2 = laps_d2["LapTime"].mean().total_seconds()

        return avg1, avg2

    def compare_simple(self, laps_d1: pd.DataFrame, laps_d2: pd.DataFrame) -> tuple[float, float] | None:

        if len(laps_d1) < 10 or len(laps_d2) < 10:
            return None

        avg1 = laps_d1["LapTime"].mean().total_seconds()
        avg2 = laps_d2["LapTime"].mean().total_seconds()

        return avg1, avg2