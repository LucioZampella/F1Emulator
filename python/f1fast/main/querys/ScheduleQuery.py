from fastf1.events import EventSchedule
from fastf1.events import Event
from fastf1.core import Session
import python.f1fast.main.querys.SessionQuery as SessionQuery
from python.f1fast.main.validators.TeamValidator import TeamValidator as tv


def get_all_racing_sessions(schedule) -> list[Session]:
    sessions = []
    for _, event in schedule.iterrows():
        try:
            sprint = event.get_sprint()
            if sprint is not None:
                sprint.load()
                sessions.append(sprint)
            race = event.get_race()
            race.load()
            sessions.append(race)
        except Exception:
            continue
    return sessions

def get_teammmates_from_schedule(team: str, sessions: list[Session]) -> list[str]:
    teammmates = []
    for session in sessions:
        tv.validate_team_exists(session.results, team)
        session_teammates = SessionQuery.get_team_drivers(team, session)
        if session_teammates != teammmates:
            teammmates = session_teammates
    return teammmates