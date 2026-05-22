import fastf1
from python.f1fast.calculators.race.race_pace_diff_calculator import FieldRacePaceCalculator
from python.f1fast.calculators.race.race_pace_diff_calculator import RacePaceDiffCalculator

session = fastf1.get_session(2025, "China", "Race")
session.load()

teams = session.results["TeamName"].unique()
calc = RacePaceDiffCalculator(session)

bilateral_results = []
for team in teams:
    result = calc.get_diff_for_team(team)
    if result is None:
        print(f"{team}: No data")
        continue
    bilateral_results.append(result)
    print(
        f"{team}: {result.faster_driver} vs {result.slower_driver} "
        f"| delta: {result.delta_pct:.3f}% "
        f"| {result.faster_driver} avg: {result.avg_driver1_seconds:.3f}s "
        f"| {result.slower_driver} avg: {result.avg_driver2_seconds:.3f}s"
    )

field_calc = FieldRacePaceCalculator(session)
paces = field_calc.get_all_driver_paces(bilateral_results)
paces.sort(key=lambda p: p.delta_to_field_pct)
print(f"Round {session.event.RoundNumber:2} ({session.event['EventName'][:20]:<20})")
for driver_pace in paces:
    print(
        f"| {driver_pace.driver} avg: {driver_pace.avg_seconds:.3f}s delta: {driver_pace.delta_to_field_pct:+.3f}% "
    )