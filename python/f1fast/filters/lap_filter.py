import pandas as pd
from fastf1.core import Laps

MIN_CLEAN_AIR_MARGIN = 1.03
KG_PER_LAP = 1.9
TIME_PER_KG = 0.020
WET_COMPOUNDS = ("Intermediate", "Wet")
MIN_GAP_AHEAD = 1.0


def filter_clean_air_laps(laps: Laps) -> Laps | None:

    laps = discard_wet_laps(laps)

    compounds = laps["Compound"].unique()

    filtered_groups = []

    session = laps.session

    for compound in compounds:

        compound_laps = laps[
            laps["Compound"] == compound
        ]

        fastest = compound_laps["LapTime"].min()

        candidate_laps = compound_laps[
            compound_laps["LapTime"] < fastest * MIN_CLEAN_AIR_MARGIN
        ]

        clean_laps = []

        for _, lap in candidate_laps.iterlaps():

            lap_start = lap["LapStartTime"]

            other_laps = session.laps[
                session.laps["Driver"] != lap["Driver"]
            ]

            previous_laps = other_laps[
                other_laps["Time"] < lap_start
            ]

            if previous_laps.empty:
                continue

            closest_car = previous_laps.sort_values(
                "Time"
            ).iloc[-1]

            gap = (
                lap_start - closest_car["Time"]
            ).total_seconds()

            if gap > MIN_GAP_AHEAD:
                clean_laps.append(lap)

        if clean_laps:
            filtered_groups.append(
                Laps(clean_laps, session=session)
            )

    if not filtered_groups:
        return None

    return Laps(
        pd.concat(filtered_groups),
        session=session
    )


def adjust_fuel_consumption(laps: Laps,
                            kg_per_lap: float = KG_PER_LAP,
                            time_per_kg: float = TIME_PER_KG) -> Laps:
    session = laps.session
    total_laps = session.total_laps
    correction = (total_laps - laps["LapNumber"]) * kg_per_lap * time_per_kg
    adjusted = laps.assign(
        LapTime=laps["LapTime"] - pd.to_timedelta(correction, unit="s")
    )
    return Laps(adjusted, session=session)


def filter_by_compound(laps: Laps, compound: str) -> Laps | None:
    result = laps[laps["Compound"] == compound]
    return None if result.empty else result


def get_common_compounds(laps1: Laps, laps2: Laps) -> set[str]:
    return set(laps1["Compound"].unique()) & set(laps2["Compound"].unique())


def get_lap_count(laps: Laps) -> int:
    return len(laps)


def get_average_seconds(laps: Laps) -> float:
    return laps["LapTime"].mean().total_seconds()

def get_weighted_avg_seconds(laps: Laps) -> float | None:
    compounds = laps["Compound"].unique()
    weighted_sum = 0.0
    total_weight = 0

    for compound in compounds:
        compound_laps = filter_by_compound(laps, compound)
        if compound_laps is None:
            continue
        adjusted = adjust_fuel_consumption(compound_laps)
        avg = get_average_seconds(adjusted)
        weight = get_lap_count(compound_laps)
        weighted_sum += avg * weight
        total_weight += weight

    if total_weight == 0:
        return None

    return weighted_sum / total_weight

def discard_wet_laps(laps: Laps) -> Laps:
    return laps[laps["Compound"] not in WET_COMPOUNDS]