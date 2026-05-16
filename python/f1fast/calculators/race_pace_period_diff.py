import statistics
import python.f1fast.exceptions.analysis_exceptions as e
import python.f1fast.queries.schedule_query as schedule_query
from python.f1fast.calculators.race_pace_diff_calculator import RacePaceDiffCalculator
from python.f1fast.domain.driver_id import DriverId
from python.f1fast.domain.race_pace_result import SeasonRacePaceDiff
from fastf1.events import EventSchedule


class RacePacePeriodDiff:

    def __init__(self, schedule: EventSchedule):
        self._sessions = schedule_query.get_all_racing_sessions(schedule)

    def get_season_diff_for_team(self, team: str) -> SeasonRacePaceDiff | None:
        gaps: list[float] = []
        driver_ids: tuple[DriverId, DriverId] | None = None

        for session in self._sessions:
            try:
                calc = RacePaceDiffCalculator(session)
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

        return SeasonRacePaceDiff(
            driver1=faster,
            driver2=slower,
            team=team,
            year=year,
            races_counted=len(gaps),
            avg_delta_pct=-abs(avg_gap),
            faster_driver=faster,
            slower_driver=slower,
        )