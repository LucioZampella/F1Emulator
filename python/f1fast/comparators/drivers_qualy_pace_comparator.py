import python.f1fast.queries.session_query as sq
from python.f1fast.domain.driver_id import DriverId
from fastf1.core import Session

def compare(session: Session, driver1_id: DriverId, driver2_id: DriverId) -> tuple[float, float, float] | None:
    driver1_time = sq.get_fastest_qualy_lap(session, driver1_id)
    driver2_time = sq.get_fastest_qualy_lap(session, driver2_id)

    if (driver1_time is None or driver2_time is None):
        return None

    faster_time = min(driver1_time, driver2_time)
    delta = ((driver1_time - driver2_time) / faster_time) * 100


    return delta, driver1_time, driver2_time