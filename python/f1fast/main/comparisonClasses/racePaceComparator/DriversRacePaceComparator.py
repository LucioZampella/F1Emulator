from fastf1.core import Laps

import python.f1fast.main.filters.LapFilter as LapFilter
import python.f1fast.main.validators.laps.LapsGuaranteer as lg
import python.f1fast.main.comparisonClasses.racePaceComparator.RPComparationMaths as maths


def compare(laps_1: Laps, laps_2: Laps) -> float | None:
    if lg.guarantee_valid_laps(laps_1, laps_2):
        return None

    both = LapFilter.get_both_compounds(laps_1, laps_2)
    final_delta = 0.0
    final_weight = 0

    for compound in both:
        temp_delta, temp_weight = maths.refactor_delta_with_ponderation(laps_1, laps_2, compound, final_weight)
        final_delta += temp_delta
        final_weight = temp_weight

    diff = final_delta / final_weight
    return diff
