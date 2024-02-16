class CustomExceptions(Exception):
    pass


class WrongNameException(CustomExceptions):
    def __init__(self, msg="Please provide name with at least 3 characters"):
        super().__init__(msg)


class WrongPhoneException(CustomExceptions):
    def __init__(self, msg="Wrong phone number"):
        super().__init__(msg)


class WrongBirthdayException(CustomExceptions):
    def __init__(self, msg="Wrong birthday value: please enter in valid format like '1990-12-20'"):
        super().__init__(msg)


class NameNotFoundException(CustomExceptions):
    def __init__(self, msg="Can't find name in phone book"):
        super().__init__(msg)


class TooSmallQueryException(CustomExceptions):
    def __init__(self, msg="Please provide query with at least 3 characters"):
        super().__init__(msg)
