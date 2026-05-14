import fastf1

from python.f1fast.main.periodDiffCalculator.RacePacePeriodDiffCalculator import RacePacePeriodDiff

schedule = fastf1.get_event_schedule(2026)
new_schedule = schedule[schedule["RoundNumber"] <= 4]
calculator = RacePacePeriodDiff(new_schedule)

first_event = new_schedule.get_event_by_round(1)
first_race = first_event.get_race()
first_race.load()
teams = first_race.results["TeamName"].unique()

for team in teams:
    result = calculator.get_season_avg_teammates_racediff_by_team(team)

    if result is None:
        print(f"No data for {team}")
        continue

    print(f"{team}: {result.faster_driver_number} vs {result.slower_driver_number} | avg delta: {result.delta}%")