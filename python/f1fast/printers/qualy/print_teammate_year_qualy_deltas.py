import fastf1
from python.f1fast.calculators.qualy.driver.session.qualy_pace_diff_calculator import QualyPaceDiffCalculator
from python.f1fast.calculators.qualy.driver.period.qualy_pace_period_diff import QualyPacePeriodDiff
import python.f1fast.queries.schedule_query as schedule_query

TEAM = ("Red Bull Racing", "McLaren")

schedule = fastf1.get_event_schedule(2024)
schedule = schedule[schedule["RoundNumber"] <= 5]
sessions = schedule_query.get_all_qualifying_sessions(schedule)

lines = []
for team in TEAM:
    for session in sessions:
        try:
            calc = QualyPaceDiffCalculator(session)
            result = calc.get_diff_for_team(team)

        except Exception as ex:
            lines.append(
                f"Round {session.event.RoundNumber:2} — ERROR: {ex}"
            )
            continue

        if result is None:
            lines.append(
                f"Round {session.event.RoundNumber:2} — None"
            )
            continue

        lines.append(
            f"Round {session.event.RoundNumber:2} "
            f"({session.event['EventName'][:20]:<20}) "
            f"| {result.driver1} avg: {result.driver1_qualy:.3f}s "
            f"| {result.driver2} avg: {result.driver2_qualy:.3f}s "
            f"| delta: {result.delta_pct:+.3f}% "
            f"| weight: {result.weight} "
            f"| faster: {result.faster_driver}"
        )

    season_calc = QualyPacePeriodDiff(schedule)
    diff = season_calc.get_season_diff_for_team(team)

    if diff is None:
        lines.append(f"\nNo data for {team}")
    else:
        lines.append(
            f"\ngap: {diff.avg_delta_pct:.3f}% "
            f"| faster: {diff.faster_driver} "
            f"| slower: {diff.slower_driver}"
        )

for line in lines:
    print(line)