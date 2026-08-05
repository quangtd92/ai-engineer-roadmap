class PlatformError(Exception):
    pass


class InvalidMessageError(PlatformError):
    pass


class ValidationError(PlatformError):
    pass
