from python.f1fast.main.comparisonClasses.dataclasses.RacePaceDiffDataclass import RacePaceDiff, SessionRacePaceDiff
from python.f1fast.main.paceDiffCalculator.RacePaceDiffCalculator import RacePaceDiffCalculator
import python.f1fast.main.querys.ScheduleQuery as ScheduleQuery
import python.f1fast.main.querys.SessionQuery as SessionQuery
from python.f1fast.main.validators.TeamValidator import TeamValidator as tv
from fastf1.core import Session
from fastf1.events import EventSchedule


class RacePacePeriodDiff:

    def __init__(self, schedule: EventSchedule):
        self.sessions = ScheduleQuery.get_all_racing_sessions(schedule)

    def get_season_avg_teammates_racediff_by_team(self, team: str, sessions: list[Session])-> RacePaceDiff | None:
        teammates = ScheduleQuery.get_teammmates_from_schedule(team, sessions)
        driver1 = teammates[0]
        driver2 = teammates[1]
        gaps = []

        for session in self.sessions:
            tv.validate_team_exists(session.results, team)
            rpdc = RacePaceDiffCalculator(session)
            if session.name == "Race":
               results = rpdc.get_rdiff_teammates_team(team)

               if results is None or results.delta is None:
                   continue

               normalized_delta = results.delta
               if results.driver1_number > results.driver2_number:
                   normalized_delta *= -1

               gaps.append(normalized_delta)

        if len(gaps) == 0:
            return None

        avg_gap = sum(gaps) / len(gaps)
        faster_driver = driver1
        slower_driver = driver2
        if avg_gap > 0:
            faster_driver = driver2
            slower_driver = driver1

        return RacePaceDiff(driver1, driver2, team, avg_gap, faster_driver, slower_driver)