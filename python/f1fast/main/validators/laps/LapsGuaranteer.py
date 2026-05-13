from fastf1.core import Laps
import python.f1fast.main.validators.laps.LapsValidator as lv

def guarantee_valid_laps(laps1: Laps, laps2: Laps) -> bool:
       return not (lv.validate_laps_arent_empty(laps1) and
        lv.validate_laps_arent_empty(laps2) and
        lv.validate_laps_in_stint_are_enough(laps1) and
        lv.validate_laps_in_stint_are_enough(laps2) and
        lv.validate_laps_comparison_are_enough(laps1, laps2))
def guarantee_stint_valid_laps(laps1: Laps, laps2: Laps) -> bool:
        return not (lv.validate_laps_in_stint_are_enough(laps1) and
        lv.validate_laps_in_stint_are_enough(laps2) and
        lv.validate_laps_comparison_are_enough(laps1, laps2))