from fastf1.core import Laps
import python.f1fast.main.filters.LapFilter as LapFilter
import python.f1fast.main.validators.laps.LapsGuaranteer as lg

def get_stint_average(laps1: Laps, laps2: Laps, compound: str) -> tuple[float, float] | None:
    laps_compound1 = LapFilter.filter_laps_for_compound(laps1, compound)
    laps_compound2 = LapFilter.filter_laps_for_compound(laps2, compound)
    laps_compound1 = LapFilter.adjust_fuel_consumption(laps_compound1)
    laps_compound2 = LapFilter.adjust_fuel_consumption(laps_compound2)

    if lg.guarantee_stint_valid_laps(laps_compound1, laps_compound2):
        return None

    return LapFilter.get_both_laps_average(laps_compound1, laps_compound2)

def refactor_delta_with_ponderation(laps1: Laps, laps2: Laps, compound: str, total_weight) -> tuple[float, int] | None:
    laps_compound1 = LapFilter.filter_laps_for_compound(laps1, compound)
    laps_compound2 = LapFilter.filter_laps_for_compound(laps2, compound)

    if lg.guarantee_stint_valid_laps(laps_compound1, laps_compound2):
        return None

    temp_avg1, temp_avg2 = get_stint_average(laps1, laps2, compound)
    temp_delta = temp_avg1 - temp_avg2
    number_laps_1 = LapFilter.get_number_of_laps(laps_compound1)
    number_laps_2 = LapFilter.get_number_of_laps(laps_compound2)

    weight = min(number_laps_1, number_laps_2)
    weighted_delta = temp_delta * weight
    total_weight += weight

    return weighted_delta, total_weight
