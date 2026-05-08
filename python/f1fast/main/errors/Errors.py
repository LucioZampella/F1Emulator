
class systemError(Exception):
    pass

class DriverNotFoundError(systemError):
    pass

class TeamNotFoundError(systemError):
    pass

class InvalidSessionError(systemError):
    pass
class InsufficientDataError(systemError):
    pass

class SessionLoadError(systemError):
    pass

class InvalidTimeFormatError(systemError):
    pass
