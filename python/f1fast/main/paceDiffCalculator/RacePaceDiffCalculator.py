import python.f1fast.main.querys.SessionQuery as sq
from python.f1fast.main.comparisonClasses.dataclasses.RacePaceDiffDataclass import SessionRacePaceDiff
from python.f1fast.main.validators.SessionValidator import SessionValidator as sv
from python.f1fast.main.validators.TeamValidator import TeamValidator as tv
from python.f1fast.main.validators.DriverValidator import DriverValidator as dv
import python.f1fast.main.comparisonClasses.racePaceComparator.DriversRacePaceComparator as drpc
import python.f1fast.main.filters.LapFilter as LapFilter
class RacePaceDiffCalculator:

    def __init__(self, session):
        self.session = session
        self.result = self.session.results

    def get_rdiff_teammates_team(self, team: str) -> SessionRacePaceDiff | None:
        tv.validate_team_exists(self.result, team)
        drivers = sq.get_team_drivers(team, self.session)
        
        sv.validate_race(self.session)
        
        driver1_number = drivers[0]
        driver2_number = drivers[1]

        laps_driver1 = sq.get_driver_clean_laps(driver1_number, self.session)
        laps_driver2 = sq.get_driver_clean_laps(driver2_number, self.session)

        if laps_driver1 is None or laps_driver2 is None:
            return None

        avg_driver1, avg_driver2 = LapFilter.get_both_laps_average(laps_driver1, laps_driver2)

        delta = drpc.compare(laps_driver1, laps_driver2)

        if avg_driver1 is None or avg_driver2 is None or delta is None:
            return None

        if delta < 0:
            faster_driver_number = driver1_number
            slower_driver_number = driver2_number
        else:
            faster_driver_number = driver2_number
            slower_driver_number = driver1_number
        
        return SessionRacePaceDiff(driver1_number, driver2_number, team, self.session,
                                   avg_driver1, avg_driver2, delta, faster_driver_number,
                                   slower_driver_number)


    def get_rdiff_teammates_driver(self, driver1_number) -> SessionRacePaceDiff | None:
        dv.validate_driver_exists(self.result, driver1_number)
        driver2 = sq.get_driver_teammate(driver1_number, self.session)

        laps_driver1 = sq.get_driver_clean_laps(driver1_number, self.session)
        laps_driver2 = sq.get_driver_clean_laps(driver2.DriverNumber, self.session)

        if laps_driver1 is None or laps_driver2 is None:
            return None

        avg_driver1, avg_driver2 = LapFilter.get_both_laps_average(laps_driver1, laps_driver2)

        delta = drpc.compare(laps_driver1, laps_driver2)

        if avg_driver1 is None or avg_driver2 is None or delta is None:
            return None

        if delta < 0:
            faster_driver_number = driver1_number
            slower_driver_number = driver2.DriverNumber
        else:
            faster_driver_number = driver2.DriverNumber
            slower_driver_number = driver1_number

        team = sq.get_driver_team(driver1_number, self.session)

        return SessionRacePaceDiff(driver1_number, driver2.DriverNumber,
                                   team, self.session, avg_driver1, avg_driver2, delta,
                                   faster_driver_number, slower_driver_number)


    #def get_rdiff_drivers(self, driver1, driver2):

    #def get_rdiff_teams(self, team1, team2):