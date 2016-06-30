
class PlayerDoesNotExist(Exception):
    pass


class TestingException(Exception):
    # raised when running tests and trying to access external apis
    pass


class CookieInvalidException(Exception):
    pass


class MatchQueryException(Exception):
    pass
