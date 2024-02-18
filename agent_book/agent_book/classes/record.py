from .book_fields import Name, Phone, Birthday, Email
from .address_entities import Address


class Record:

    def __init__(self, name):
        self.__name = Name(name)
        self._birthday = None
        self._email = None
        self._address = None
        self.phones = []

    @property
    def name(self) -> Name:
        return self.__name

    def update_name(self, name: str):
        self.__name = Name(name)

    @property
    def email(self) -> Email:
        return self._email

    @email.setter
    def email(self, email: Email):
        self._email = Email(email)

    @property
    def birthday(self) -> Birthday:
        return self._birthday

    @birthday.setter
    def birthday(self, birthday: Birthday):
        self._birthday = Birthday(birthday)

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    def address(self, address: Address):
        self._address = address

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
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
        ret = f"Agent name: {self.name.value}"
        if self.email is not None:
            ret += f", email: {self.email}"
        if self.birthday is not None:
            ret += f", birthday: {str(self.birthday)}, days to birth: {self.days_to_birthday()}"
        if len(self.phones):
            ret += f", {'phones' if len(self.phones) > 1 else 'phone'}: {'; '.join(p.value for p in self.phones)}"
        if self.address is not None:
            ret += f", address: {str(self.address)}"
        return ret
