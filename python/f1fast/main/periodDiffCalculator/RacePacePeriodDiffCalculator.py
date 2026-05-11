from python.f1fast.main.comparisonClasses.RacePaceDiffDataclass import RacePaceDiff
from python.f1fast.main.paceDiffCalculator.RacePaceDiffCalculator import RacePaceDiffCalculator
from python.f1fast.main.querys.SessionQuery import SessionQuerys
import fastf1
from python.f1fast.main.querys.ScheduleQuery import ScheduleQuery
from python.f1fast.main.validators.TeamValidator import TeamValidator as tv


class RacePacePeriodDiff:

    def __init__(self, year: int):
        self.year = year
        schedule = fastf1.get_event_schedule(year)
        sq = ScheduleQuery(schedule)
        self.sessions = sq.get_all_race_sessions()

    def get_season_avg_teammates_racediff_by_team(self, team: str) -> RacePaceDiff | None:
        results = []
        faster_driver_number = None
        slower_driver_number = None
        drivernumber_1 = None
        drivernumber_2 = None

        for race in self.sessions:
            try:
                tv.validate_team_exists(race.results, team)
                calculator = RacePaceDiffCalculator(race)
                diff = calculator.get_rdiff_teammates_team(team)

                if diff is not None:
                    results.append(diff.delta)
                    faster_driver_number = diff.faster_driver_number
                    slower_driver_number = diff.slower_driver_number
                    drivernumber_1 = diff.driver1_number
                    drivernumber_2 = diff.driver2_number

            except Exception:
                continue

        if not results or drivernumber_1 is None:
            return None

        delta = sum(results) / len(results)
        return RacePaceDiff(drivernumber_1, drivernumber_2, team, delta, faster_driver_number, slower_driver_number)