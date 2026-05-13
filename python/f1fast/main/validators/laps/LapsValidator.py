import pandas as pd
from fastf1.core import Laps
import python.f1fast.main.errors.Errors as e

def validate_laps_arent_empty(laps: Laps) -> bool:
    return (laps is not None)

def validate_laps_in_stint_are_enough(laps: Laps) -> bool:
    if (validate_laps_arent_empty(laps)):
        return len(laps["LapTime"].values) >= 8
    else:
        return False

def validate_laps_comparison_are_enough(laps1: Laps, laps2: Laps) -> bool:

    total_laps1 = len(laps1["LapTime"].values)
    total_laps2 = len(laps2["LapTime"].values)

    max_value= max(total_laps1, total_laps2)
    min_value= min(total_laps1, total_laps2)

    return (max_value / min_value) <= 2.5
