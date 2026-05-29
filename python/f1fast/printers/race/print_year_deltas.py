import fastf1
from python.f1fast.calculators.race.driver.period.race_pace_period_diff import RacePacePeriodDiff, SeasonFieldPace

schedule = fastf1.get_event_schedule(2023)

#schedule = schedule[schedule["RoundNumber"] <= 4]

calculator = RacePacePeriodDiff(schedule)
first_event = schedule.get_event_by_round(1)
first_race = first_event.get_race()
first_race.load()
teams = first_race.results["TeamName"].unique()

for team in teams:
    result = calculator.get_season_diff_for_team(team)
    if result is None:
        print(f"No data for {team}")
        continue
    print(
        f"{team}: {result.faster_driver} vs {result.slower_driver} "
        f"| avg delta: {result.avg_delta_pct:.3f}% "
        f"| races: {result.races_counted}"
    )

print("\nSeason Field Pace")
field_calculator = SeasonFieldPace(schedule)
season_paces = field_calculator.get_season_field_pace()

if season_paces is None:
    print("No data")
else:
    for pace in season_paces:
        print(
            f"{pace.driver} ({pace.team}) "
            f"| avg delta: {pace.avg_delta_to_field_pct:+.3f}% "
            f"| races: {pace.races_counted}"
        )