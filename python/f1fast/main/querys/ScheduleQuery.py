

class ScheduleQuery:
    def __init__(self, event_schedule):
        self.event_schedule = event_schedule

    def get_all_race_sessions(self) -> list:
        sessions = []
        for _, event in self.event_schedule.iterrows():
            try:
                race = event.get_race()
                race.load()
                sessions.append(race)
            except Exception:
                continue
        return sessions