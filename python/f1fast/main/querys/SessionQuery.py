import fastf1
import errors.Errors as e
from validators.F1Validator import F1Validator

class SessionQuerys:

    def __init__(self, session):
        self.session = session


    def get_driver_teammate(self, driver_number: str) -> str:
        results = self.session.results

        F1Validator.validate_driver_exists(results, driver_number)

        teamnameFilter = results["DriverNumber"] == driver_number
        driver_team = results[teamnameFilter]["TeamName"].iloc[0]

        teammate = None
        filter = (results["TeamName"] == driver_team) & (results["DriverNumber"] != driver_number)
        filtered = results[filter]

        if filtered.empty:
            raise e.DriverNotFoundError(f"Driver {driver_number} teammate was not found in this session")
        else:
            teammate = filtered["DriverNumber"].iloc[0]

        return teammate

    def get_driver_number_from_lastname(self, driver_lastname: str) -> str:
        results = self.session.results

        if driver_lastname not in results["LastName"].values:
            raise e.DriverNotFoundError(f"Driver {driver_lastname} not found in this session")

        filter = results["LastName"] == driver_lastname
        return results[filter]["DriverNumber"].iloc[0]

    def get_driver_racepace(self, driver_number: str) -> str:
        results = self.session.results

        F1Validator.validate_driver_exists(results, driver_number)
        





