

class systemError(Exception):
    pass

class DriverNotFoundError(systemError):
    pass

class InsufficientDataError(systemError):
    pass

class sessionLoadError(systemError):
    pass
