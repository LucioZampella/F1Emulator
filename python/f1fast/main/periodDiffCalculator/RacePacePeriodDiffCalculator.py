from python.f1fast.main.comparisonClasses.dataclasses.RacePaceDiffDataclass import RacePaceDiff
from python.f1fast.main.paceDiffCalculator.RacePaceDiffCalculator import RacePaceDiffCalculator
import fastf1
from python.f1fast.main.querys.ScheduleQuery import ScheduleQuery
from python.f1fast.main.validators.TeamValidator import TeamValidator as tv


class RacePacePeriodDiff:

    def __init__(self, schedule):
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

                if diff is not None and diff.delta is not None:
                    driver1_as_int = int(diff.driver1_number)
                    driver2_as_int = int(diff.driver2_number)

                    if driver1_as_int > driver2_as_int:
                        normalized_delta = -diff.delta
                        drivernumber_1 = diff.driver2_number
                        drivernumber_1 = diff.driver1_number
                    else:
                        normalized_delta = diff.delta
                        drivernumber_1 = diff.driver1_number
                        drivernumber_2 = diff.driver2_number

                    results.append(normalized_delta)

                    faster_driver_number = diff.faster_driver_number
                    slower_driver_number = diff.slower_driver_number


            except Exception as e:
                print(f"{team} | {race.event['EventName']} | {e}")
                continue

        if not results:
            return None

        delta = sum(results) / len(results)
        return RacePaceDiff(drivernumber_1, drivernumber_2, team, delta, faster_driver_number, slower_driver_number)