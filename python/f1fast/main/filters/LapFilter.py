import pandas as pd
from fastf1.core import Laps


class LapFilter:

    def filter_clean_air_laps(self, driver_laps: Laps) -> Laps | None:
        driver_compounds = list(driver_laps["Compound"].unique())
        fastest_lap_per_compound = dict()
        for compound in driver_compounds:
            driver_laps_in_compound = driver_laps[driver_laps["Compound"] == compound]
            fastest_lap = driver_laps_in_compound["LapTime"].min()
            fastest_lap_per_compound[compound] = fastest_lap

        temp = []
        for compound, fastest_lap in fastest_lap_per_compound.items():
            driver_clean_air_laps = driver_laps[(driver_laps["Compound"] == compound) & (driver_laps["LapTime"] < fastest_lap * 1.03)]
            if not driver_clean_air_laps.empty:
                temp.append(driver_clean_air_laps)

        if not temp:
            return None

        return Laps(
            pd.concat(temp),
            session=driver_laps.session
        )


    def adjust_fuel_consumption(self, laps_d1: Laps,
                                kg_per_lap: float = 1.9, time_per_kg: float = 0.020) -> Laps | None:

        if laps_d1 is None:
            return None

        session = laps_d1.session
        laps_of_session = session.total_laps
        correction = (laps_of_session - laps_d1["LapNumber"]) * kg_per_lap * time_per_kg
        adjusted = laps_d1.assign(
            LapTime=laps_d1["LapTime"] - pd.to_timedelta(correction, unit="s")
        )

        return Laps(adjusted, session=session)
