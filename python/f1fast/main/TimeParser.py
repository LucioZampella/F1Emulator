import pandas as pd
from python.f1fast.main.validators.FormatValidator import FormatValidator as fv

class TimeParser:

    @staticmethod
    def get_lap_in_seconds(original_time):
        if pd.notna(original_time):
            fv.validate_qualy_lap_input_format(original_time)
            return original_time.total_seconds()
        else:
            return 99999999999999