import re
from datetime import date, datetime

from .field import Field, validator
from ..exceptions import WrongBirthdayException, WrongNameException, WrongPhoneException
from ..enums import DATE_FORMAT


class Name(Field):
    def _validate(self, value):
        if not (isinstance(value, str) and len(value) >= 3):
            raise WrongNameException


class Phone(Field):
    def _validate(self, value):
        pattern = r'\b\d{10}\b'
        if not bool(re.search(pattern, value)):
            raise WrongPhoneException


class Birthday(Field):

    @staticmethod
    def __convert_to_date(date_str: str):
        return datetime.strptime(date_str, DATE_FORMAT).date()

    @Field.value.setter
    @validator
    def value(self, value):
        self._value = self.__convert_to_date(value)

    def _validate(self, value: str):
        try:
            birthday = self.__convert_to_date(value)
        except ValueError:
            raise WrongBirthdayException

        if birthday > date.today():
            raise WrongBirthdayException("Birthday have to be in the past")

    def days_to_birthday(self) -> int:
        today = date.today()
        this_year_birth = date(today.year, self.value.month, self.value.day)
        if this_year_birth < today:
            next_year_birth = date(today.year + 1, self.value.month, self.value.day)
            days_until_birth = (next_year_birth - today).days
        else:
            days_until_birth = (this_year_birth - today).days

        return days_until_birth

    def __str__(self):
        return self._value.strftime(DATE_FORMAT)
