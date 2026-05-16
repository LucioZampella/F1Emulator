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