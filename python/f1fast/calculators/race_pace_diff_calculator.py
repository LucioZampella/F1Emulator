from fastf1.core import Session
from python.f1fast.domain.driver_id import DriverId
from python.f1fast.domain.race_pace_result import SessionRacePaceDiff
import python.f1fast.exceptions.analysis_exceptions as e
import python.f1fast.queries.session_query as session_query
import python.f1fast.comparators.drivers_race_pace_comparator as comparator
import python.f1fast.filters.lap_filter as lap_filter

VALID_SESSION_TYPES = ("Race", "Sprint")


class RacePaceDiffCalculator:

    def __init__(self, session: Session):
        if session.name not in VALID_SESSION_TYPES:
            raise e.InvalidSessionError(
                expected=str(VALID_SESSION_TYPES),
                received=session.name
            )
        self._session = session

    def get_diff_for_team(self, team: str) -> SessionRacePaceDiff | None:
        driver1_id, driver2_id = session_query.get_team_driver_ids(team, self._session)
        return self._compute_diff(driver1_id, driver2_id, team)

    def get_diff_for_driver(self, driver_id: DriverId) -> SessionRacePaceDiff | None:
        teammate_id = session_query.get_teammate_id(driver_id, self._session)
        team = session_query.get_driver_team(driver_id, self._session)
        return self._compute_diff(driver_id, teammate_id, team)

    def _compute_diff(self, driver1: DriverId, driver2: DriverId,
                      team: str) -> SessionRacePaceDiff | None:
        laps1 = session_query.get_driver_clean_laps(driver1, self._session)
        laps2 = session_query.get_driver_clean_laps(driver2, self._session)

        if laps1 is None or laps2 is None:
            return None

        delta = comparator.compare(laps1, laps2)

        if delta is None:
            return None

        avg1 = lap_filter.get_average_seconds(laps1)
        avg2 = lap_filter.get_average_seconds(laps2)

        faster = driver1 if delta < 0 else driver2
        slower = driver2 if delta < 0 else driver1

        return SessionRacePaceDiff(
            driver1=faster,
            driver2=slower,
            team=team,
            session_name=self._session.name,
            year=self._session.event.year,
            round_number=self._session.event.RoundNumber,
            avg_driver1_seconds=avg1,
            avg_driver2_seconds=avg2,
            delta_pct=-abs(delta),
            faster_driver=faster,
            slower_driver=slower,
        )