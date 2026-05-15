from fastf1.core import Laps

import python.f1fast.main.filters.LapFilter as LapFilter
import python.f1fast.main.validators.laps.LapsGuaranteer as lg
import python.f1fast.main.comparisonClasses.racePaceComparator.RPComparationMaths as maths


def compare(laps_1: Laps, laps_2: Laps) -> float | None:
    if not lg.guarantee_valid_laps(laps_1, laps_2):
        return None

    both = LapFilter.get_both_compounds(laps_1, laps_2)
    weighted_delta_sum = 0.0
    total_weight = 0

    for compound in both:
        result = maths.refactor_delta_with_ponderation(laps_1, laps_2, compound)
        if result is None:
            continue

        weighted_delta, weight, faster_avg = result

        delta_pct = (weighted_delta / faster_avg) * 100
        weighted_delta_sum += delta_pct * weight
        total_weight += weight
    if total_weight == 0:
        return None

    return weighted_delta_sum / total_weight
