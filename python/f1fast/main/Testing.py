import fastf1

import python.f1fast.main.filters.LapFilter as LapFilter
from python.f1fast.main.querys.SessionQuery import SessionQuerys as sq
from python.f1fast.main.paceDiffCalculator.RacePaceDiffCalculator import RacePaceDiffCalculator
from python.f1fast.main.periodDiffCalculator.RacePacePeriodDiffCalculator import RacePacePeriodDiff

session = fastf1.get_session(2026, "Miami", "Race")
session.load()
query = sq(session)
calculator = RacePaceDiffCalculator(session)
drivers = session.drivers
results = session.results
drivers_already_passed = []
for d in drivers:
    teammate = query.get_driver_teammate(d)
    if teammate.DriverNumber not in drivers_already_passed:

        driver = results[results["DriverNumber"] == d].iloc[0]
        print(f"In this session, {driver.LastName} teammate was {teammate.LastName}")

        all_driver_quicklaps = session.laps.pick_drivers(driver.DriverNumber).pick_quicklaps().reset_index()
        all_teammate_quicklaps = session.laps.pick_drivers(teammate.DriverNumber).pick_quicklaps().reset_index()
        driver_quicklaps = all_driver_quicklaps["LapTime"].mean().total_seconds()
        teammate_quicklaps = all_teammate_quicklaps["LapTime"].mean().total_seconds()
        gap_ql = driver_quicklaps - teammate_quicklaps

        driver_cal = calculator.get_rdiff_teammates_driver(d)
        if driver_cal is None:
            print(f"No clean air laps available from {driver.LastName} \n")
            continue

        print(f"Quicklaps: \n {driver.LastName}: {driver_quicklaps} | {teammate.LastName}: {teammate_quicklaps} | Gap: {gap_ql}")
        print(f"CleanAirLaps: \n {driver.LastName}: {driver_cal.avg_driver1} | {teammate.LastName}: {driver_cal.avg_driver2} | Gap: {driver_cal.delta}\n")
        drivers_already_passed.append(d)