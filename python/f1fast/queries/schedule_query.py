import logging
from fastf1.core import Session
from fastf1.events import EventSchedule

logger = logging.getLogger(__name__)


def get_all_racing_sessions(schedule: EventSchedule) -> list[Session]:

    sessions = []

    for _, event in schedule.iterrows():
        try:
            sprint = event.get_sprint()
            sprint.load()
            sessions.append(sprint)
        except Exception as ex:
            logger.debug(f"Sin sprint en {event['EventName']}: {ex}")

        try:
            race = event.get_race()
            race.load()
            sessions.append(race)
        except Exception as ex:
            logger.warning(f"No se pudo cargar la carrera de {event['EventName']}: {ex}")

    return sessions

def get_all_qualifying_sessions(schedule: EventSchedule) -> list[Session]:

    sessions = []
    year = schedule.iloc[0]["EventDate"].year

    for _, event in schedule.iterrows():
        try:
            if year >= 2024:
                sprint_qualy = event.get_sprint_qualifying()
            else:
                sprint_qualy = event.get_sprint_shootout()
            sprint_qualy.load()
            sessions.append(sprint_qualy)
        except Exception as ex:
            logger.debug(f"Sin qualy sprint en {event['EventName']}: {ex}")
        try:
            qualy = event.get_qualifying()
            qualy.load()
            sessions.append(qualy)
        except Exception as ex:
            logger.warning(f"No se pudo cargar la qualy de {event['EventName']}: {ex}")

    return sessions