from address_book.exceptions import CustomExceptions, WrongNameException, WrongPhoneException, WrongBirthdayException, \
    NameNotFoundException, TooSmallQueryException
from address_book.fs import datadir
from collections import UserDict
from datetime import date, datetime
import re
import pickle


def validator(setter_func):
    def wrapper(self, value):
        try:
            is_valid = self._validate(value)
        except CustomExceptions as e:
            raise e
        # if raise exception is not realized in validate function lets raise it
        if isinstance(is_valid, bool) and not is_valid:
            raise ValueError(f"{self.__class__.__name__}: Invalid value: {value}")

        return setter_func(self, value)

    return wrapper


DATE_FORMAT = '%Y-%m-%d'


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def _validate(self, value):
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    @validator
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)


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


class Record:
    birthday = None

    def __init__(self, name, birthday: str = None):
        self.name = Name(name)
        if birthday is not None:
            self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
        return self

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)
        return self

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError('Phone not found')

    def edit_phone(self, phone, new_phone):
        self.remove_phone(phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        found_phone = list(filter(lambda ph: ph.value == phone, self.phones))
        return found_phone[0] if len(found_phone) else None

    def is_query_in_phones(self, query) -> bool:
        found_phone = list(filter(lambda ph: query in ph.value, self.phones))
        return bool(len(found_phone))

    def days_to_birthday(self):
        if self.birthday is not None:
            return self.birthday.days_to_birthday()

    def __str__(self):
        ret = f"Contact name: {self.name.value},"
        if self.birthday is not None:
            ret += f" birthday: {str(self.birthday)}, days to birth: {self.days_to_birthday()},"
        return f"{ret} phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    dump_file_name = datadir() / 'address_book.bin'

    @staticmethod
    def serialize(obj):
        with open(AddressBook.dump_file_name, "wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def deserialize():
        try:
            with open(AddressBook.dump_file_name, "rb") as file:
                obj = pickle.load(file)
            return obj
        except FileNotFoundError:
            return AddressBook()

    def add(self, name, phone, birthday: str = None):
        self.add_record(Record(name=name, birthday=birthday).add_phone(phone))

    def add_record(self, record):
        self.data[record.name.value] = record

    def find_record(self, name) -> Record:
        return self.data.get(name, None)

    def find(self, query):
        if len(query) < 3:
            raise TooSmallQueryException
        in_names = [name for name in self.data.keys() if query.lower() in name.lower()]
        in_phones = [record.name.value for record in self.data.values() if record.is_query_in_phones(query)]
        all_names = list(set(in_names + in_phones))
        return [self.data.get(key) for key in all_names] if len(all_names) > 0 else []

    def delete(self, name):
        self.data.pop(name, None)

    def add_phone(self, name, phone):
        record = self.find_record(name)
        if record is not None:
            record.add_phone(str(phone))
        else:
            raise NameNotFoundException

    def add_birthday(self, name: str, birthday: str):
        record = self.find_record(name)
        if record is not None:
            record.add_birthday(str(birthday))
        else:
            raise NameNotFoundException

    def get_phones(self, name) -> list[Phone]:
        record = self.find_record(name)
        if record is not None:
            return record.phones
        else:
            raise NameNotFoundException
