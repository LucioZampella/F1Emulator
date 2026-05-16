import pandas as pd
from fastf1.core import Laps

MIN_CLEAN_AIR_MARGIN = 1.03
KG_PER_LAP = 1.9
TIME_PER_KG = 0.020


def filter_clean_air_laps(laps: Laps) -> Laps | None:
    compounds = laps["Compound"].unique()

    filtered_groups = []
    for compound in compounds:
        compound_laps = laps[laps["Compound"] == compound]
        fastest = compound_laps["LapTime"].min()
        clean = compound_laps[compound_laps["LapTime"] < fastest * MIN_CLEAN_AIR_MARGIN]
        if not clean.empty:
            filtered_groups.append(clean)

    if not filtered_groups:
        return None

    return Laps(pd.concat(filtered_groups), session=laps.session)


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