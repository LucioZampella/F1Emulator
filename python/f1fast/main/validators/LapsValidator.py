import pandas as pd
import python.f1fast.main.errors.Errors as e


class LapsValidator:

    @staticmethod
    def validate_clean_air_laps_are_enough(laps: pd.DataFrame) -> e:
        if laps.empty:
            return None