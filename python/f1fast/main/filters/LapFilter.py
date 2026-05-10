import pandas as pd



class LapFilter:

    def filter_clean_air_laps(self, driver_laps: pd.DataFrame, all_laps: pd.DataFrame,
                              dirty_air_gap: float = 1.5) -> pd.DataFrame:

        driver_times = driver_laps[["Driver", "LapNumber", "LapStartTime"]]
        all_times = all_laps[["Driver", "LapNumber", "LapStartTime"]]

        merged = driver_times.merge(all_times, on="LapNumber", suffixes=("", "_other"))
        merged = merged[merged["Driver"] != merged["Driver_other"]]

        merged = merged.assign(
            gap=(merged["LapStartTime"] - merged["LapStartTime_other"]).abs().dt.total_seconds()
        )

        min_gaps = merged.groupby(["Driver", "LapNumber"])["gap"].min()
        clean = min_gaps[min_gaps > dirty_air_gap].reset_index()

        return driver_laps.merge(clean[["Driver", "LapNumber"]], on=["Driver", "LapNumber"])

    def adjust_fuel_consumption(self, laps_d1: pd.DataFrame, laps_d2: pd.DataFrame,
                                kg_per_lap: float = 1.9, time_per_kg: float = 0.020) -> tuple[
        pd.DataFrame, pd.DataFrame]:

        compounds_both = set(laps_d1["Compound"].unique()) & set(laps_d2["Compound"].unique())

        result_d1, result_d2 = [], []

        for compound in compounds_both:
            comp_d1 = laps_d1[laps_d1["Compound"] == compound].copy()
            comp_d2 = laps_d2[laps_d2["Compound"] == compound].copy()

            lap_diff = comp_d1["LapNumber"].mean() - comp_d2["LapNumber"].mean()
            correction = abs(lap_diff) * kg_per_lap * time_per_kg

            if lap_diff < 0:
                comp_d1 = comp_d1.assign(
                    LapTime=comp_d1["LapTime"] + pd.to_timedelta(correction, unit="s")
                )
            else:
                comp_d2 = comp_d2.assign(
                    LapTime=comp_d2["LapTime"] + pd.to_timedelta(correction, unit="s")
                )

            result_d1.append(comp_d1)
            result_d2.append(comp_d2)

        if not result_d1 or not result_d2:
            return pd.DataFrame(), pd.DataFrame()

        return pd.concat(result_d1), pd.concat(result_d2)

    def filter_comparable_stints(self, laps_driver_1: pd.DataFrame, laps_driver_2: pd.DataFrame) -> tuple[
        pd.DataFrame, pd.DataFrame]:
        compound_d1 = set(laps_driver_1["Compound"].unique())
        compound_d2 = set(laps_driver_2["Compound"].unique())
        compounds_both = compound_d1 & compound_d2

        result_d1, result_d2 = [], []

        for compound in compounds_both:
            stints_d1 = laps_driver_1[laps_driver_1["Compound"] == compound]["Stint"].unique()
            stints_d2 = laps_driver_2[laps_driver_2["Compound"] == compound]["Stint"].unique()

            for s1, s2 in zip(stints_d1, stints_d2):
                stint_laps_d1 = laps_driver_1[
                    (laps_driver_1["Compound"] == compound) & (laps_driver_1["Stint"] == s1)
                    ]
                stint_laps_d2 = laps_driver_2[
                    (laps_driver_2["Compound"] == compound) & (laps_driver_2["Stint"] == s2)
                    ]

                limit = min(stint_laps_d1["TyreLife"].max(), stint_laps_d2["TyreLife"].max())

                filtered_d1 = stint_laps_d1[stint_laps_d1["TyreLife"] <= limit]
                filtered_d2 = stint_laps_d2[stint_laps_d2["TyreLife"] <= limit]

                if not filtered_d1.empty and not filtered_d2.empty:
                    result_d1.append(filtered_d1)
                    result_d2.append(filtered_d2)

        if not result_d1 or not result_d2:
            return pd.DataFrame(), pd.DataFrame()

        return pd.concat(result_d1), pd.concat(result_d2)

    def filter_consecutive_tyre_laps(self, laps: pd.DataFrame, max_gap: int = 3) -> pd.DataFrame:
        result = []
        for stint in laps["Stint"].unique():
            stint_laps = laps[laps["Stint"] == stint].sort_values("TyreLife")
            tyre_diff = stint_laps["TyreLife"].diff()
            # si hay un gap mayor a max_gap, quedamos solo con el bloque más largo
            split_points = tyre_diff[tyre_diff > max_gap].index
            if len(split_points) == 0:
                result.append(stint_laps)
            else:
                # tomamos el bloque más largo de laps consecutivos
                blocks = []
                prev = 0
                indices = list(split_points) + [None]
                for idx in indices:
                    block = stint_laps.loc[prev:idx].iloc[:-1] if idx else stint_laps.loc[prev:]
                    blocks.append(block)
                    prev = idx
                result.append(max(blocks, key=len))
        return pd.concat(result) if result else pd.DataFrame()

