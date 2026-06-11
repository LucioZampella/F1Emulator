from fastf1.core import Laps, Session, SessionResults
import python.f1fast.exceptions.analysis_exceptions as e
import python.f1fast.filters.lap_filter as lap_filter
from python.f1fast.domain.driver_id import DriverId
import python.f1fast.validators.session_validator as sv
import pandas as pd


def _get_result_row(driver_id: DriverId, session: Session):
    results = session.results
    mask = results["Abbreviation"] == driver_id.abbreviation
    filtered = results[mask]
    if filtered.empty:
        raise e.DriverNotFoundError(str(driver_id), session.name)
    return filtered.iloc[0]


def get_team_driver_ids(team: str, session: Session) -> tuple[DriverId, DriverId]:
    results = session.results
    mask = results["TeamName"] == team
    team_results = results[mask]

    if team_results.empty:
        raise e.TeamNotFoundError(team, session.name)

    drivers = [
        DriverId.from_result_row(row)
        for _, row in team_results.iterrows()
    ]

    if len(drivers) != 2:
        raise e.TeammatesNotFoundError(team, found=len(drivers))

    drivers.sort(key=lambda d: d.abbreviation)
    return drivers[0], drivers[1]


def get_teammate_id(driver_id: DriverId, session: Session) -> DriverId:
    row = _get_result_row(driver_id, session)
    team = row["TeamName"]

    results = session.results
    mask = (results["TeamName"] == team) & (results["Abbreviation"] != driver_id.abbreviation)
    filtered = results[mask]

    if filtered.empty:
        raise e.DriverNotFoundError(f"compañero de {driver_id}", session.name)

    return DriverId.from_result_row(filtered.iloc[0])


def get_driver_team(driver_id: DriverId, session: Session) -> str:
    row = _get_result_row(driver_id, session)
    return row["TeamName"]


def get_driver_clean_laps(driver_id: DriverId, session: Session) -> Laps | None:
    _get_result_row(driver_id, session)
    all_laps = session.laps.pick_quicklaps()
    driver_laps = all_laps.pick_drivers(driver_id.abbreviation)
    return lap_filter.filter_clean_air_laps(driver_laps)


def get_driver_id_from_lastname(lastname: str, session: Session) -> DriverId:
    results = session.results
    mask = results["LastName"] == lastname
    filtered = results[mask]

    if filtered.empty:
        raise e.DriverNotFoundError(lastname, session.name)

    return DriverId.from_result_row(filtered.iloc[0])


def get_driver_compounds(driver_id: DriverId, session: Session) -> list[str]:
    laps = session.laps.pick_drivers(driver_id.abbreviation)
    return list(laps["Compound"].unique())


def get_fastest_qualy_lap(session: Session, driver_id: DriverId) -> float | None:
    if sv.is_wet_session(session):
        return None
    year = session.date.year
    if year >= 2024:
        if not sv.is_qualifying_session_after_2023(session):
            raise e.InvalidSessionError("Qualifying", "Race")
    else:
        if not sv.is_qualifying_session_before_2023(session):
            raise e.InvalidSessionError("Qualifying", "Race")

    results = session.results
    row = results[results["Abbreviation"] == driver_id.abbreviation].iloc[0]

    for q in ["Q3", "Q2", "Q1"]:
        val = row[q]
        if not pd.isna(val):
            return val.total_seconds()

    return None

def get_fastest_comparables_lap(session: Session, driver_id_1: DriverId, driver_id_2) -> list[float] | None:
    if sv.is_wet_session(session):
        return None
    year = session.date.year
    if year >= 2024:
        if not sv.is_qualifying_session_after_2023(session):
            raise e.InvalidSessionError("Qualifying", "Race")
    else:
        if not sv.is_qualifying_session_before_2023(session):
            raise e.InvalidSessionError("Qualifying", "Race")

    results = session.results
    row_1 = results[results["Abbreviation"] == driver_id_1.abbreviation].iloc[0]
    row_2 = results[results["Abbreviation"] == driver_id_2.abbreviation].iloc[0]

    for q in ["Q3", "Q2", "Q1"]:
        val_1 = row_1[q]
        val_2 = row_2[q]
        if not pd.isna(val_1) and not pd.isna(val_2):
            return [val_1.total_seconds(), val_2.total_seconds()]

    return None