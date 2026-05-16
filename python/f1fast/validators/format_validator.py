import pandas as pd
import python.f1fast.exceptions.analysis_exceptions as e


def assert_valid_timedelta(time) -> None:
    if not isinstance(time, pd.Timedelta):
        raise e.InvalidTimeFormatError(
            f"Se esperaba pd.Timedelta, se recibió {type(time).__name__}"
        )