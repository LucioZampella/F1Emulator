import fastf1

from python.f1fast.main.filters.LapFilter import LapFilter
from python.f1fast.main.querys.SessionQuery import SessionQuerys as sq
from python.f1fast.main.paceDiffCalculator.RacePaceDiffCalculator import RacePaceDiffCalculator
from python.f1fast.main.periodDiffCalculator.RacePacePeriodDiffCalculator import RacePacePeriodDiff

schedule = fastf1.get_event_schedule(2025)
schedule = schedule[schedule["RoundNumber"] <= 5]
calculator = RacePacePeriodDiff(2025)

first_event = schedule.get_event_by_round(1)
first_race = first_event.get_race()
first_race.load()
teams = first_race.results["TeamName"].unique()

for team in teams:
    result = calculator.get_season_avg_teammates_racediff_by_team(team)

    if result is None:
        print(f"No data for {team}")
        continue

    print(f"{team}: {result.faster_driver_number} vs {result.slower_driver_number} | avg delta: {result.delta:.3f}s")