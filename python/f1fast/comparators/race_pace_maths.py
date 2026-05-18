from fastf1.core import Laps
import python.f1fast.filters.lap_filter as lap_filter
import python.f1fast.validators.laps_validator as validator


def compute_weighted_delta(laps1: Laps, laps2: Laps,
                           compound: str) -> tuple[float, int, float, float, float] | None:
    laps_c1 = lap_filter.filter_by_compound(laps1, compound)
    laps_c2 = lap_filter.filter_by_compound(laps2, compound)

    if laps_c1 is None or laps_c2 is None:
        return None

    if not validator.pair_is_valid(laps_c1, laps_c2):
        return None

    avg1, avg2 = _get_fuel_adjusted_averages(laps_c1, laps_c2)
    if avg1 is None or avg2 is None:
        return None

    faster_avg = min(avg1, avg2)
    delta = avg1 - avg2
    weight = min(lap_filter.get_lap_count(laps_c1), lap_filter.get_lap_count(laps_c2))

    return delta, weight, faster_avg, avg1, avg2

def _get_fuel_adjusted_averages(laps1: Laps,
                                laps2: Laps) -> tuple[float, float] | None:

    adjusted1 = lap_filter.adjust_fuel_consumption(laps1)
    adjusted2 = lap_filter.adjust_fuel_consumption(laps2)

    if not validator.pair_is_valid(adjusted1, adjusted2):
        return None

    return lap_filter.get_average_seconds(adjusted1), lap_filter.get_average_seconds(adjusted2)