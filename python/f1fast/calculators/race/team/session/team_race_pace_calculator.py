from python.f1fast.domain.driver_pace_result import DriverRacePace
from python.f1fast.domain.team_pace_result import TeamRacePace

def get_all_team_paces(paces: list[DriverRacePace]) -> list[TeamRacePace]:
    team_paces = dict()
    team_drivers = dict()
    for driver_pace in paces:
        if driver_pace.team not in team_paces:
            team_paces[driver_pace.team] = (driver_pace.avg_seconds / 2)
            team_drivers[driver_pace.team] = [driver_pace]
        else:
            team_paces[driver_pace.team] += (driver_pace.avg_seconds / 2)
            team_drivers[driver_pace.team].append(driver_pace)

    return (sorted([
        TeamRacePace(
            team=team,
            drivers=team_drivers[team],
            session_name=paces[0].session_name,
            year=paces[0].year,
            round_number=paces[0].round_number,
            pace=pace,
            delta_to_field_pct=((pace - get_reference(paces)) / get_reference(paces)) * 100
        ) for team, pace in team_paces.items()
    ], key=lambda x: x.delta_to_field_pct
    ))



def get_pace_for_a_team(paces: list[DriverRacePace], team: str) -> TeamRacePace:

    team_drivers = []
    for driver_pace in paces:
        if driver_pace.team == team:
            team_drivers.append(driver_pace)

    pace = (sum(team_drivers) / len(team_drivers))

    return TeamRacePace(
        team=team,
        drivers=team_drivers,
        session_name=paces[0].session_name,
        year=paces[0].year,
        round_number=paces[0].round_number,
        pace=pace,
        delta_to_field_pct=((pace - get_reference(paces)) / get_reference(paces)) * 100
    )

def get_reference(paces: list[DriverRacePace]) -> float:

    teams_pace = dict()
    for driver_pace in paces:
        if driver_pace.team not in teams_pace:
            teams_pace[driver_pace.team] = (driver_pace.avg_seconds / 2)
        else:
            teams_pace[driver_pace.team] += (driver_pace.avg_seconds / 2)
    return teams_pace[min(teams_pace, key=teams_pace.get)]