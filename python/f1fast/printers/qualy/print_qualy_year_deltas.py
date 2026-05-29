import fastf1
from python.f1fast.calculators.qualy.driver.period.qualy_pace_period_diff import (
    QualyPacePeriodDiff,
    SeasonFieldQualyPace
)
from python.f1fast.calculators.qualy.team.period.team_qualy_pace_period_calculator import (
    SeasonFieldTeamQualyPace
)

schedule = fastf1.get_event_schedule(2024)
#schedule = schedule[schedule["RoundNumber"] <= 21]
#schedule = schedule[schedule["RoundNumber"] >= 15]

lines = []

calculator = QualyPacePeriodDiff(schedule)

first_event = schedule.get_event_by_round(15)
first_race = first_event.get_race()
first_race.load()

teams = first_race.results["TeamName"].unique()

for team in teams:
    result = calculator.get_season_diff_for_team(team)

    if result is None:
        lines.append(f"No data for {team}")
        continue

    lines.append(
        f"{team}: {result.faster_driver} vs {result.slower_driver} "
        f"| avg delta: {result.avg_delta_pct:.3f}% "
        f"| races: {result.races_counted}"
    )

lines.append("\nSeason Field Pace")

field_calculator = SeasonFieldQualyPace(schedule)
season_paces = field_calculator.get_season_field_pace()

if season_paces is None:
    lines.append("No data")
else:
    for pace in season_paces:
        lines.append(
            f"{pace.driver} ({pace.team}) "
            f"| avg delta: {pace.avg_delta_to_field_pct:+.3f}% "
            f"| races: {pace.races_counted}"
        )

lines.append("\nSeason Team Qualy Pace")

team_calculator = SeasonFieldTeamQualyPace(schedule)
season_team_paces = team_calculator.get_season_field_team_pace()

if season_team_paces is None:
    lines.append("No data")
else:
    for pace in season_team_paces:
        lines.append(
            f"{pace.team} "
            f"| avg delta: {pace.avg_delta_to_field_pct:+.3f}% "
            f"| races: {pace.races_counted}"
        )

for line in lines:
    print(line)