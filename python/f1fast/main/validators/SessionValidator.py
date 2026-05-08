import python.f1fast.main.errors.Errors as e

class SessionValidator:

    @staticmethod
    def validate_session(session) -> e:
        if session.name != "Qualifying" and session.name != "Race":
            raise e.InvalidSessionError(f"Session {session.name} must be a race or a qualy")

    @staticmethod
    def validate_official_qualy(session) -> e:
        if session.name != "Qualifying":
            raise e.InvalidSessionError(f"Session {session.name} must be a qualy")

    @staticmethod
    def validate_qualy(session) -> e:
        if session.name != "Qualifying" and session.name != "Sprint Shootout" and session.name != "Sprint Qualifying":
            raise e.InvalidSessionError(f"Session {session.name} must be a qualifying session")

    @staticmethod
    def validate_official_race(session) -> e:
        if session.name != "Race":
            raise e.InvalidSessionError(f"Session {session.name} must be a race")

    @staticmethod
    def validate_race(session) -> e:
        if session.name != "Race" and session.name != "Sprint":
            raise e.InvalidSessionError(f"Session {session.name} must be a race session")