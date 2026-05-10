from python.f1fast.main.querys.SessionQuery import SessionQuerys
from python.f1fast.main.comparisonClasses.RacePaceDiffDataclass import RacePaceDiff
from python.f1fast.main.validators.SessionValidator import SessionValidator as sv
from python.f1fast.main.validators.TeamValidator import TeamValidator as tv
from python.f1fast.main.comparisonClasses.DriversPaceComparator import DriversPaceComparator
from python.f1fast.main.filters.LapFilter import LapFilter
class RacePaceDiffCalculator:

    def __init__(self, session):
        self.session = session
        self.sq = SessionQuerys(self.session)
        self.result = self.session.results
        self.lf = LapFilter()
        self.dpc = DriversPaceComparator(self.lf)

    def get_rdiff_teammates_team(self, team: str) -> RacePaceDiff | None:
        tv.validate_team_exists(self.result, team)
        drivers = self.sq.get_team_drivers(team)
        
        sv.validate_race(self.session)
        
        driver1_number = drivers[0]
        driver2_number = drivers[1]
        
        avg_driver1 = self.sq.get_driver_clean_laps(driver1_number)
        avg_driver2 = self.sq.get_driver_clean_laps(driver2_number)

        if avg_driver1 is None or avg_driver2 is None:
            return None

        result = self.dpc.compare_simple(avg_driver1, avg_driver2)

        if result is None:
            return None

        avg_driver1, avg_driver2 = result

        avg_min = min(avg_driver1, avg_driver2)
        avg_max = max(avg_driver1, avg_driver2)
        
        delta = avg_min - avg_max

        if avg_min == avg_driver1:
            faster_driver_number = driver1_number
            slower_driver_number = driver2_number
        else:
            faster_driver_number = driver2_number
            slower_driver_number = driver1_number
        
        return RacePaceDiff(driver1_number, driver2_number, team, self.session, avg_driver1, avg_driver2, delta, faster_driver_number, slower_driver_number)


    #def get_rdiff_teammates_driver(self, driver_number):

    #def get_rdiff_drivers(self, driver1, driver2):

    #def get_rdiff_teams(self, team1, team2):