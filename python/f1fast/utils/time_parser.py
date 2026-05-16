import pandas as pd
from python.f1fast.validators.format_validator import assert_valid_timedelta

TIME = 99999999999999.0


def parse_qualy_lap_seconds(time) -> float:
    if pd.isna(time):
        return TIME
    assert_valid_timedelta(time)
    return time.total_seconds()