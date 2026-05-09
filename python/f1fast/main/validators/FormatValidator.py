import pandas as pd
import python.f1fast.main.errors.Errors as e

class FormatValidator:

    @staticmethod
    def validate_qualy_lap_input_format(time):
        if not isinstance(time, pd.Timedelta):
            raise e.InvalidTimeFormatError("Invalid time format")