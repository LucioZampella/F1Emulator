import statistics

from fastf1.core import Session
from python.f1fast.domain.driver_id import DriverId
from python.f1fast.domain.driver_pace_result import SessionRacePaceDiff
import python.f1fast.exceptions.analysis_exceptions as e
import python.f1fast.queries.session_query as session_query
import python.f1fast.comparators.drivers_race_pace_comparator as comparator
import python.f1fast.filters.lap_filter as lap_filter
from python.f1fast.domain.driver_pace_result import DriverRacePace
import python.f1fast.validators.laps_validator as validator

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

        result = comparator.compare(laps1, laps2)
        if result is None:
            return None

        delta, avg1, avg2 = result

        faster = driver1 if delta < 0 else driver2
        slower = driver2 if delta < 0 else driver1
        avg_faster = avg1 if delta < 0 else avg2
        avg_slower = avg2 if delta < 0 else avg1

        return SessionRacePaceDiff(
            driver1=faster,
            driver2=slower,
            team=team,
            session_name=self._session.name,
            year=self._session.event.year,
            round_number=self._session.event.RoundNumber,
            avg_driver1_seconds=avg_faster,
            avg_driver2_seconds=avg_slower,
            delta_pct=-abs(delta),
            faster_driver=faster,
            slower_driver=slower,
        )

class FieldRacePaceCalculator:

    def __init__(self, session: Session):
        if session.name not in VALID_SESSION_TYPES:
            raise e.InvalidSessionError(
                expected=str(VALID_SESSION_TYPES),
                received=session.name
            )
        self._session = session

    def get_all_driver_paces(self, bilateral_results: list[SessionRacePaceDiff]) -> list[DriverRacePace] | None:
        driver_avgs: dict[DriverId, tuple[str, float]] = {}

        for result in bilateral_results:
            driver_avgs[result.driver1] = (result.team, result.avg_driver1_seconds)
            driver_avgs[result.driver2] = (result.team, result.avg_driver2_seconds)

        for _, row in self._session.results.iterrows():
            driver_id = DriverId.from_result_row(row)
            if driver_id in driver_avgs:
                continue
            team = row["TeamName"]
            laps = session_query.get_driver_clean_laps(driver_id, self._session)
            if not validator.laps_are_sufficient(laps):
                continue
            avg = lap_filter.get_weighted_avg_seconds(laps)
            if avg is None:
                continue
            driver_avgs[driver_id] = (team, avg)

        if not driver_avgs:
            return None

        ref_avg = min(avg for _, avg in driver_avgs.values())

        return [
            DriverRacePace(
                driver=driver_id,
                team=team,
                session_name=self._session.name,
                year=self._session.event.year,
                round_number=self._session.event.RoundNumber,
                avg_seconds=avg,
                delta_to_field_pct=(avg - ref_avg) / ref_avg * 100,
            )
            for driver_id, (team, avg) in driver_avgs.items()
        ]