from fastf1.core import Laps

MIN_LAPS_FOR_STINT = 8
MAX_LAPS_RATIO = 2.5


def laps_are_sufficient(laps: Laps | None) -> bool:
    if laps is None or laps.empty:
        return False
    return len(laps) >= MIN_LAPS_FOR_STINT


def laps_are_balanced(laps1: Laps, laps2: Laps) -> bool:
    count1 = len(laps1)
    count2 = len(laps2)
    ratio = max(count1, count2) / min(count1, count2)
    return ratio <= MAX_LAPS_RATIO


def pair_is_valid(laps1: Laps | None, laps2: Laps | None) -> bool:
    if not laps_are_sufficient(laps1) or not laps_are_sufficient(laps2):
        return False
    return laps_are_balanced(laps1, laps2)