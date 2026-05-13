import pandas as pd
from fastf1.core import Laps
import python.f1fast.main.validators.laps.LapsValidator as lv

def filter_clean_air_laps(laps: Laps) -> Laps | None:
    driver_compounds = list(laps["Compound"].unique())
    fastest_lap_per_compound = dict()
    for compound in driver_compounds:
        laps_in_compound = laps[laps["Compound"] == compound]
        fastest_lap = laps_in_compound["LapTime"].min()
        fastest_lap_per_compound[compound] = fastest_lap

    temp = []
    for compound, fastest_lap in fastest_lap_per_compound.items():
        driver_clean_air_laps = laps[(laps["Compound"] == compound) & (laps["LapTime"] < fastest_lap * 1.03)]
        if not driver_clean_air_laps.empty:
            temp.append(driver_clean_air_laps)

    if not temp:
        return None

    return Laps(
        pd.concat(temp),
        session=laps.session
    )


def adjust_fuel_consumption(laps_1: Laps,
    kg_per_lap: float = 1.9, time_per_kg: float = 0.020) -> Laps | None:

    if laps_1 is None:
        return None

    session = laps_1.session
    laps_of_session = session.total_laps
    correction = (laps_of_session - laps_1["LapNumber"]) * kg_per_lap * time_per_kg
    adjusted = laps_1.assign(
        LapTime=laps_1["LapTime"] - pd.to_timedelta(correction, unit="s")
    )

    return Laps(adjusted, session=session)

def filter_laps_for_compound(laps: Laps, compound: str) -> Laps | None:
    if lv.validate_laps_arent_empty(laps):
        return None
    return laps[laps["Compound"] == compound]

def get_both_compounds(laps1: Laps, laps2: Laps) -> set:
    laps1 = set(laps1["Compound"].unique())
    laps2 = set(laps2["Compound"].unique())
    return (laps1 & laps2)

def get_both_laps_average(laps1: Laps, laps2: Laps) -> tuple[float, float]:
    avg1 = laps1["LapTime"].mean().total_seconds()
    avg2 = laps2["LapTime"].mean().total_seconds()
    return avg1, avg2

def get_number_of_laps(laps1: Laps) -> int:
    return len(laps1["LapTime"].values)