import statistics

import python.f1fast.exceptions.analysis_exceptions as e
import python.f1fast.queries.schedule_query as schedule_query

from fastf1.events import EventSchedule

from python.f1fast.calculators.qualy.driver.session.qualy_pace_diff_calculator import (
    QualyPaceDiffCalculator,
    FieldQualyPaceCalculator
)

from python.f1fast.calculators.qualy.team.session.team_qualy_pace_calculator import (
    get_all_team_paces
)

from python.f1fast.domain.team_pace_result import SeasonTeamQualyPace


class SeasonFieldTeamQualyPace:

    def __init__(self, schedule: EventSchedule):
        self._sessions = schedule_query.get_all_qualifying_sessions(schedule)

    def get_season_field_team_pace(self) -> list[SeasonTeamQualyPace] | None:

        team_deltas: dict[str, list[float]] = {}

        for session in self._sessions:

            try:
                diff_calc = QualyPaceDiffCalculator(session)

                teams = session.results["TeamName"].unique()

                bilateral_results = []

                for team in teams:

                    try:
                        result = diff_calc.get_diff_for_team(team)

                    except Exception:
                        continue

                    if result is not None:
                        bilateral_results.append(result)

                field_calc = FieldQualyPaceCalculator(session)

                driver_paces = field_calc.get_all_driver_paces(
                    bilateral_results
                )

                if driver_paces is None:
                    continue

                team_paces = get_all_team_paces(driver_paces)

            except e.F1AnalysisError:
                continue

            except Exception:
                continue

            for pace in team_paces:

                if pace.team not in team_deltas:
                    team_deltas[pace.team] = []

                team_deltas[pace.team].append(
                    pace.delta_to_field_pct
                )

        if not team_deltas:
            return None

        return sorted([

            SeasonTeamQualyPace(
                team=team,
                year=self._sessions[0].event.year,
                races_counted=len(deltas),
                avg_delta_to_field_pct=statistics.mean(deltas)
            )

            for team, deltas in team_deltas.items()

        ], key=lambda x: x.avg_delta_to_field_pct)