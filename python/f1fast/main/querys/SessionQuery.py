import fastf1
import python.f1fast.main.errors.Errors as e
from python.f1fast.main.validators.DriverValidator import DriverValidator as dv
from python.f1fast.main.validators.SessionValidator import SessionValidator as sv
from python.f1fast.main.validators.TeamValidator import TeamValidator as tv
from python.f1fast.main.TimeParser import TimeParser as tp

class SessionQuerys:

    def __init__(self, session):
        self.session = session


    def get_driver_teammate(self, driver_number: str):
        results = self.session.results

        dv.validate_driver_exists(results, driver_number)

        teamnameFilter = results["DriverNumber"] == driver_number
        driver_team = results[teamnameFilter]["TeamName"].iloc[0]

        teammate = None
        filter = (results["TeamName"] == driver_team) & (results["DriverNumber"] != driver_number)
        filtered = results[filter]

        if filtered.empty:
            raise e.DriverNotFoundError(f"Driver {driver_number} teammate was not found in this session")
        else:
            teammate = filtered.iloc[0]
        return teammate

    def get_driver_number_from_lastname(self, driver_lastname: str) -> str:
        results = self.session.results

        if driver_lastname not in results["LastName"].values:
            raise e.DriverNotFoundError(f"Driver {driver_lastname} not found in this session")

        filter = results["LastName"] == driver_lastname
        return results[filter]["DriverNumber"].iloc[0]


    def get_driver_qualifying_pace(self, driver_number: str) -> float:
        results = self.session.results

        dv.validate_driver_exists(results, driver_number)
        sv.validate_qualy(self.session)

        filter = results["DriverNumber"] == driver_number
        qualy_laps = []
        i = 1
        while i < 4:
            time = results[filter][f"Q{i}"].iloc[0]
            lap = tp.get_lap_in_seconds(time)
            qualy_laps.append(lap)
            i += 1

        return min(qualy_laps)

    def get_team_drivers(self, team_name: str) -> list:
        results = self.session.results
        tv.validate_team_exists(results, team_name)
        filter = results["TeamName"] = team_name
        return list(results[filter]["DriverNumber"])


