import fastf1
from python.f1fast.calculators.qualy.qualy_pace_diff_calculator import QualyPaceDiffCalculator
import python.f1fast.queries.schedule_query as schedule_query

TEAM = "Aston Martin"

schedule = fastf1.get_event_schedule(2025)
sessions = schedule_query.get_all_qualifying_sessions(schedule)

for session in sessions:
    try:
        calc = QualyPaceDiffCalculator(session)
        result = calc.get_diff_for_team(TEAM)
    except Exception as ex:
        print(f"Round {session.event.RoundNumber:2} — ERROR: {ex}")
        continue

    if result is None:
        print(f"Round {session.event.RoundNumber:2} — None")
        continue

    print(
        f"Round {session.event.RoundNumber:2} ({session.event['EventName'][:20]:<20}) "
        f"| {result.driver1} avg: {result.driver1_qualy:.3f}s "
        f"| {result.driver2} avg: {result.driver2_qualy:.3f}s "
        f"| delta: {result.delta_pct:+.3f}% "
        f"| faster: {result.faster_driver}"
    )