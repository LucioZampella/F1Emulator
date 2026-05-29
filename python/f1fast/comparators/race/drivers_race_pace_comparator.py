from fastf1.core import Laps
import python.f1fast.filters.lap_filter as lap_filter
import python.f1fast.validators.laps_validator as validator
import python.f1fast.comparators.race.race_pace_maths as maths


def compare(laps_1: Laps, laps_2: Laps) -> tuple[float, float, float] | None:
    if not validator.pair_is_valid(laps_1, laps_2):
        return None

    common_compounds = lap_filter.get_common_compounds(laps_1, laps_2)
    weighted_delta_sum = 0.0
    weighted_avg1_sum = 0.0
    weighted_avg2_sum = 0.0
    total_weight = 0

    for compound in common_compounds:
        result = maths.compute_weighted_delta(laps_1, laps_2, compound)
        if result is None:
            continue

        weighted_delta, weight, faster_avg, avg1, avg2 = result
        delta_pct = (weighted_delta / faster_avg) * 100
        weighted_delta_sum += delta_pct * weight
        weighted_avg1_sum += avg1 * weight
        weighted_avg2_sum += avg2 * weight
        total_weight += weight

    if total_weight == 0:
        return None

    return (
        weighted_delta_sum / total_weight,
        weighted_avg1_sum / total_weight,
        weighted_avg2_sum / total_weight,
    )