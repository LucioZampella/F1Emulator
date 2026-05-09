import fastf1
from python.f1fast.main.querys.SessionQuery import SessionQuerys as sq

session = fastf1.get_session(2026, "China", "Qualifying")
session.load()
query = sq(session)
drivers = session.drivers
results = session.results
for d in drivers:
    teammate = query.get_driver_teammate(d)
    driver = results[results["DriverNumber"] == d].iloc[0]
    print(f"In this session, {driver.FullName} teammate was {teammate.FullName}")

for d in drivers:
    driver=results[results["DriverNumber"] == d].iloc[0]
    time = query.get_driver_qualifying_pace(d)
    print(f"{driver.FullName} qualifying time was {time}")