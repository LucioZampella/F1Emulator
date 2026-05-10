import fastf1

from python.f1fast.main.filters.LapFilter import LapFilter
from python.f1fast.main.querys.SessionQuery import SessionQuerys as sq
from python.f1fast.main.paceDiffCalculator.RacePaceDiffCalculator import RacePaceDiffCalculator

session = fastf1.get_session(2026, "Miami", "Race")
session.load()
query = sq(session)
calculator = RacePaceDiffCalculator(session)
drivers = session.drivers
results = session.results
for d in drivers:
    teammate = query.get_driver_teammate(d)
    driver = results[results["DriverNumber"] == d].iloc[0]
    print(f"In this session, {driver.FullName} teammate was {teammate.FullName}")

print("\n")

teams = results["TeamName"].unique()
teams_already_calculated = []
for team in teams:
    pace = calculator.get_rdiff_teammates_team(team)

    if pace is None:
        print(f"No comparable data for {team}")
        continue


    print(f"In this session, for {team}, the faster driver was {pace.faster_driver_number}"
          f" against {pace.slower_driver_number} over {pace.delta} sgs")

    print(f"\n=== {team} ===")
    print(f"Faster: {pace.faster_driver_number} vs {pace.slower_driver_number} | Delta: {pace.delta:.3f}s")


    all_laps = session.laps.pick_quicklaps()
    results = session.results
    drivers = results[results["TeamName"] == team]["DriverNumber"].values

    for driver in drivers:
        d_laps = all_laps.pick_drivers(driver)
        clean = calculator.lf.filter_clean_air_laps(d_laps, all_laps)
        print(f"\nDriver {driver} - Quicklaps: {len(d_laps)} | Clean: {len(clean)}")
        if not clean.empty:
            comp_d1, comp_d2 = calculator.lf.filter_comparable_stints(
                calculator.sq.get_driver_clean_laps(drivers[0]),
                calculator.sq.get_driver_clean_laps(drivers[1])
            )
            print(f"Comparable {drivers[0]}: {len(comp_d1)} | {drivers[1]}: {len(comp_d2)}")
            print(f"Compuestos: {clean['Compound'].unique()}")
            print(clean[["LapNumber", "Compound", "TyreLife", "LapTime"]].to_string())
            break

    teams_already_calculated.append(team)

