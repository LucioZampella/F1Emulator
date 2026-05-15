from fastf1.core import Laps
from fastf1.core import Session

import python.f1fast.main.errors.Errors as e
from python.f1fast.main.validators.DriverValidator import DriverValidator as dv
from python.f1fast.main.validators.SessionValidator import SessionValidator as sv
from python.f1fast.main.validators.TeamValidator import TeamValidator as tv
from python.f1fast.main.TimeParser import TimeParser as tp
import python.f1fast.main.filters.LapFilter as LapFilter

def get_driver_teammate(driver_number: str, session: Session):
    results = session.results

    dv.validate_driver_exists(results, driver_number)

    teamnameFilter = results["DriverNumber"] == driver_number
    driver_team = results[teamnameFilter]["TeamName"].iloc[0]

    teammate = None
    filter = (results["TeamName"] == driver_team) & (results["DriverNumber"] != driver_number)
    filtered = results[filter]

    if filtered.empty:
        raise e.DriverNotFoundError(f"Driver {driver_number} teammate was not found in this session")
    else:
        teammate = filtered.iloc[0]
    return teammate

def get_driver_number_from_lastname(driver_lastname: str, session: Session) -> str:
    results = session.results

    if driver_lastname not in results["LastName"].values:
        raise e.DriverNotFoundError(f"Driver {driver_lastname} not found in this session")

    filter = results["LastName"] == driver_lastname
    return results[filter]["DriverNumber"].iloc[0]


def get_driver_qualifying_pace(driver_number: str, session: Session) -> float:
    results = session.results

    dv.validate_driver_exists(results, driver_number)
    sv.validate_qualy(session)

    filter = results["DriverNumber"] == driver_number
    qualy_laps = []
    i = 1
    while i < 4:
        time = results[filter][f"Q{i}"].iloc[0]
        lap = tp.get_qualy_lap_in_seconds(time)
        qualy_laps.append(lap)
        i += 1
    return min(qualy_laps)

def get_driver_clean_laps(driver_number: str, session: Session) -> Laps | None:
    results = session.results

    dv.validate_driver_exists(results, driver_number)
    sv.validate_race(session)

    all_laps = session.laps.pick_quicklaps()
    driver_laps = all_laps.pick_drivers(driver_number)
    clean_laps = LapFilter.filter_clean_air_laps(driver_laps)
    return clean_laps

def get_team_drivers(team_name: str, session: Session) -> list:
    results = session.results
    tv.validate_team_exists(results, team_name)
    filter = results["TeamName"] == team_name
    drivers = sorted(results[filter]["DriverNumber"], key=int)
    return list(drivers)

def get_driver_team(driver_number: str, session: Session) -> str:
    results = session.results

    dv.validate_driver_exists(results, driver_number)

    teamnameFilter = results["DriverNumber"] == driver_number
    driver_team = results[teamnameFilter]["TeamName"].iloc[0]

    return driver_team

def get_driver_compounds_at_session(driver_number: str, session: Session) -> list:
    laps = session.laps.pick_drivers(driver_number)
    return list(laps["Compound"].unique())
