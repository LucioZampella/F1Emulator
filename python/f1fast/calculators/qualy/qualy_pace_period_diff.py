import statistics
import python.f1fast.exceptions.analysis_exceptions as e
import python.f1fast.queries.schedule_query as schedule_query
from python.f1fast.calculators.qualy.qualy_pace_diff_calculator import QualyPaceDiffCalculator, FieldQualyPaceCalculator
from python.f1fast.domain.driver_id import DriverId
from python.f1fast.domain.driver_pace_result import SeasonQualyPaceDiff, SeasonDriverQualyPace
from fastf1.events import EventSchedule


class QualyPacePeriodDiff:

    def __init__(self, schedule: EventSchedule):
        self._sessions = schedule_query.get_all_qualifying_sessions(schedule)

    def get_season_diff_for_team(self, team: str) -> SeasonQualyPaceDiff | None:
        gaps: list[float] = []
        driver_ids: tuple[DriverId, DriverId] | None = None

        for session in self._sessions:
            try:
                calc = QualyPaceDiffCalculator(session)
                result = calc.get_diff_for_team(team)
            except e.InvalidSessionError:
                continue
            except e.TeamNotFoundError:
                continue
            except e.F1AnalysisError:
                continue

            if result is None:
                continue

            if driver_ids is None:
                d1, d2 = sorted(
                    [result.driver1, result.driver2],
                    key=lambda d: d.abbreviation
                )
                driver_ids = (d1, d2)

            canonical_d1 = driver_ids[0]
            if result.driver1 == canonical_d1:
                normalized_delta = result.delta_pct
            else:
                normalized_delta = -result.delta_pct

            gaps.append(normalized_delta)

        if not gaps or driver_ids is None:
            return None

        avg_gap = statistics.mean(gaps)
        d1, d2 = driver_ids
        faster = d1 if avg_gap < 0 else d2
        slower = d2 if avg_gap < 0 else d1
        year = self._sessions[0].event.year

        return SeasonQualyPaceDiff(
            driver1=faster,
            driver2=slower,
            team=team,
            year=year,
            races_counted=len(gaps),
            avg_delta_pct=-abs(avg_gap),
            faster_driver=faster,
            slower_driver=slower,
        )


class SeasonFieldQualyPace:

    def __init__(self, schedule: EventSchedule):
        self._sessions = schedule_query.get_all_qualifying_sessions(schedule)

    def get_season_field_pace(self) -> list[SeasonDriverQualyPace] | None:
        driver_deltas: dict[DriverId, list[float]] = {}
        driver_teams: dict[DriverId, str] = {}

        for session in self._sessions:
            try:
                calc = QualyPaceDiffCalculator(session)
                teams = session.results["TeamName"].unique()
                bilateral_results = []
                for team in teams:
                    try:
                        result = calc.get_diff_for_team(team)
                    except Exception:
                        continue
                    if result is not None:
                        bilateral_results.append(result)

                field_calc = FieldQualyPaceCalculator(session)
                paces = field_calc.get_all_driver_paces(bilateral_results)
            except Exception:
                continue

            if paces is None:
                continue

            for pace in paces:
                if pace.driver not in driver_deltas:
                    driver_deltas[pace.driver] = []
                    driver_teams[pace.driver] = pace.team
                driver_deltas[pace.driver].append(pace.delta_to_field_pct)

        if not driver_deltas:
            return None

        return sorted([
            SeasonDriverQualyPace(
                driver=driver_id,
                team=driver_teams[driver_id],
                year=self._sessions[0].event.year,
                races_counted=len(deltas),
                avg_delta_to_field_pct=statistics.mean(deltas),
            )
            for driver_id, deltas in driver_deltas.items()
        ], key=lambda x: x.avg_delta_to_field_pct)