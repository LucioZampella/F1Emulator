import fastf1
from python.f1fast.calculators.qualy.driver.session.qualy_pace_diff_calculator import QualyPaceDiffCalculator
from python.f1fast.calculators.qualy.driver.session.qualy_pace_diff_calculator import FieldQualyPaceCalculator
import python.f1fast.calculators.qualy.team.session.team_qualy_pace_calculator as team_calculator
session = fastf1.get_session(2026, "Monaco", "Qualifying")
session.load()
teams = session.results["TeamName"].unique()
calc = QualyPaceDiffCalculator(session)

results = []
for team in teams:
    result = calc.get_diff_for_team(team)
    if result is None:
        print(f"{team}: No data")
        continue
    results.append(result)
    print(
        f"{team}: {result.faster_driver} vs {result.slower_driver} "
        f"| delta: {result.delta_pct:.3f}% "
        f"| {result.faster_driver} avg: {result.driver1_qualy:.3f}s "
        f"| {result.slower_driver} avg: {result.driver2_qualy:.3f}s"
    )

field_calc = FieldQualyPaceCalculator(session)
paces = field_calc.get_all_driver_paces(results)
paces.sort(key=lambda p: p.delta_to_field_pct)
print(f"Round {session.event.RoundNumber:2} ({session.event['EventName'][:20]:<20})")
for driver_pace in paces:
    print(
        f"| {driver_pace.driver} avg: {driver_pace.qualy_time:.3f}s delta: {driver_pace.delta_to_field_pct:+.3f}% "
    )

team_paces = team_calculator.get_all_team_paces(paces)
for team in team_paces:
    print(f"| {team.team} | pace: {team.pace: .3f}s | delta: {team.delta_to_field_pct: .3f}%")