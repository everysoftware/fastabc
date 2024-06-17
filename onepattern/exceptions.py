class OPException(Exception):
    pass


class OPNoResultFound(OPException):
    pass


class OPMultipleResultsFound(OPException):
    pass


class OPValueError(OPException, ValueError):
    pass
