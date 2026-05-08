import errors.Errors as e

class F1Validator:

    @staticmethod
    def validate_driver_exists(results, driver_number: str) -> e:
        if driver_number not in results["DriverNumber"].values:
            raise e.DriverNotFoundError(f"Driver {driver_number} not found in this session")