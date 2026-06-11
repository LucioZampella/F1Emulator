from fastf1.core import Session
from python.f1fast.domain.driver_id import DriverId
import python.f1fast.queries.session_query as session_query
from python.f1fast.domain.driver_pace_result import DriverQualyPace, SessionQualyPaceDiff
import python.f1fast.comparators.qualy.drivers_qualy_pace_comparator as comparator
import python.f1fast.validators.session_validator as sv

class QualyPaceDiffCalculator:

    def __init__(self, session: Session):
        self._session = session

    def get_diff_for_team(self, team: str) -> SessionQualyPaceDiff:
        driver1_id, driver2_id = session_query.get_team_driver_ids(team, self._session)
        return self._compute_diff(driver1_id, driver2_id, team)

    def get_diff_for_driver(self, driver_id: DriverId) -> SessionQualyPaceDiff | None:
        teammate_id = session_query.get_teammate_id(driver_id, self._session)
        team = session_query.get_driver_team(driver_id, self._session)
        return self._compute_diff(driver_id, teammate_id, team)

    def _compute_diff(self, driver1: DriverId, driver2: DriverId,
                      team: str) -> SessionQualyPaceDiff | None:

        result = comparator.compare(self._session, driver1, driver2)

        if result is None:
            return None

        delta, driver1_time, driver2_time = result

        if abs(delta) > 2.0:
            return None

        if sv.is_sprint_q(self._session):
            weight = 0.25
        else:
            weight = 1.00

        faster = driver1 if delta < 0 else driver2
        slower = driver2 if delta < 0 else driver1
        time_faster = driver1_time if delta < 0 else driver2_time
        time_slower = driver2_time if delta < 0 else driver1_time

        return SessionQualyPaceDiff(
            driver1 = faster,
            driver2 = slower,
            team = team,
            session_name = self._session.name,
            year=self._session.event.year,
            round_number=self._session.event.RoundNumber,
            delta_pct=-abs(delta),
            driver1_qualy=time_faster,
            driver2_qualy=time_slower,
            faster_driver=faster,
            slower_driver=slower,
            weight=weight
        )

class FieldQualyPaceCalculator:

    def __init__(self, session: Session):
        self._session = session

    def get_all_driver_paces(self, results: list[SessionQualyPaceDiff]) -> list[DriverQualyPace] | None:
        driver_pace: dict[DriverId, tuple[str, float]] = {}

        driver_teams: dict[DriverId, str] = {}
        for result in results:
            driver_teams[result.driver1] = result.team
            driver_teams[result.driver2] = result.team

        for driver_id, team in driver_teams.items():
            best = session_query.get_fastest_qualy_lap(self._session, driver_id)
            if best is not None:
                driver_pace[driver_id] = (team, best)

        if not driver_pace:
            return None

        ref_time = min(time for _, time in driver_pace.values())

        return [
            DriverQualyPace(
                driver=driver_id,
                team=team,
                session_name=self._session.name,
                year=self._session.event.year,
                round_number=self._session.event.RoundNumber,
                qualy_time=time,
                delta_to_field_pct=(time - ref_time) / ref_time * 100,
            )
            for driver_id, (team, time) in driver_pace.items()
        ]