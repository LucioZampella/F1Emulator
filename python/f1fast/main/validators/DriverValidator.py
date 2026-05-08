import python.f1fast.main.errors.Errors as e

class DriverValidator:

    @staticmethod
    def validate_driver_exists(results, driver_number: str) -> e:
        if driver_number not in results["DriverNumber"].values:
            raise e.DriverNotFoundError(f"Driver {driver_number} was not found in this session")