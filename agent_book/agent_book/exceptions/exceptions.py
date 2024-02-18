from .main_exception import AgentBookException


class EnumValueNotExist(AgentBookException):
    pass


class WrongCountryException(AgentBookException):
    def __init__(self, msg="Please provide right country name. We support only Україна and USA"):
        super().__init__(msg)


class WrongNameException(AgentBookException):
    def __init__(self, msg="Please provide name with at least 3 characters"):
        super().__init__(msg)


class WrongNameLengthException(AgentBookException):
    def __init__(self, field, max_len = 50):
        super().__init__(f'Please provide {field} with at least 3 characters and no more than {max_len} characters')


class WrongPhoneException(AgentBookException):
    def __init__(self, msg="Wrong phone number"):
        super().__init__(msg)


class WrongBirthdayException(AgentBookException):
    def __init__(self, msg="Wrong birthday value: please enter in valid format like '1990-12-20'"):
        super().__init__(msg)


class NameNotFoundException(AgentBookException):
    def __init__(self, msg="Can't find name in phone book"):
        super().__init__(msg)


class TooSmallQueryException(AgentBookException):
    def __init__(self, msg="Please provide query with at least 3 characters"):
        super().__init__(msg)
