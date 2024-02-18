import pickle
from collections import UserDict

from ..fs import datadir
from .record import Record
from .book_fields import Phone
from ..exceptions import TooSmallQueryException, NameNotFoundException


class AgentBook(UserDict):
    dump_file_name = datadir() / 'agent_book.bin'

    @staticmethod
    def serialize(obj):
        with open(AgentBook.dump_file_name, "wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def deserialize():
        try:
            with open(AgentBook.dump_file_name, "rb") as file:
                obj = pickle.load(file)
            return obj
        except FileNotFoundError:
            return AgentBook()

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
            record.birthday = str(birthday)
        else:
            raise NameNotFoundException

    def get_phones(self, name) -> list[Phone]:
        record = self.find_record(name)
        if record is not None:
            return record.phones
        else:
            raise NameNotFoundException
