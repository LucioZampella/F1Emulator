# python/f1fast/exceptions.py

class F1AnalysisError(Exception):
    pass

class InvalidSessionError(F1AnalysisError):
    def __init__(self, expected: str, received: str):
        super().__init__(f"Session '{expected}' was expected,'{received}' was received instead")
        self.expected = expected
        self.received = received


class DriverNotFoundError(F1AnalysisError):
    def __init__(self, driver_id: str, session_name: str):
        super().__init__(f"Driver '{driver_id}' was not found at session '{session_name}'")
        self.driver_id = driver_id
        self.session_name = session_name


class TeamNotFoundError(F1AnalysisError):
    def __init__(self, team: str, session_name: str):
        super().__init__(f"The team '{team}' was not found at session '{session_name}'")
        self.team = team
        self.session_name = session_name


class TeammatesNotFoundError(F1AnalysisError):
    def __init__(self, team: str, found: int):
        super().__init__(f"Two drivers was expected for '{team}', {found} driver was found instead")
        self.team = team
        self.found = found

class InvalidTimeFormatError(F1AnalysisError):
    """Formato de tiempo inválido. Bug de entrada de datos."""

class ConfigurationError(F1AnalysisError):
    pass