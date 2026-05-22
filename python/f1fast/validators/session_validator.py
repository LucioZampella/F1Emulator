import pandas as pd
import python.f1fast.exceptions.analysis_exceptions as e
from fastf1.core import Session

QUALIFYING_SESSIONS_NOW = ("Qualifying", "Sprint Qualifying")
QUALIFYING_SESSIONS_BEFORE = ("Qualifying", "Sprint Shootout")
WET_COMPOUNDS = ("Intermediate", "Wet")


def is_qualifying_session_before_2023(session: Session) -> bool:
    if (session.name in QUALIFYING_SESSIONS_BEFORE):
        return True
    return False

def is_qualifying_session_after_2023(session: Session) -> bool:
    if (session.name in QUALIFYING_SESSIONS_NOW):
        return True
    return False

def is_wet_session(session: Session) -> bool:
    compounds = session.laps["Compound"]
    for values in compounds:
        if values in WET_COMPOUNDS:
            return True
    return False