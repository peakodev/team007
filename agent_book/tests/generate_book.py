from faker import Faker
from random import randint, choice
from datetime import date, timedelta
from agent_book import (AgentBook, Record, PaginatedAgentBookIterator, Address, DATE_FORMAT,
                        AgentBookException, UKRAINIAN_REGIONS, CallSignNotFoundException, AgentBookIterator)


book = AgentBook()


def test_change_call_sign():
    book.add('nazariy')
    book.add('nazar')

    try:
        book.add('nazar')
    except AgentBookException as inst:
        print(str(inst))

    book.change_call_sign('nazar', 'nazarko')

    try:
        book.change_call_sign('nazarko', 'nazariy')
    except AgentBookException as inst:
        print(str(inst))

    book.add('Вʼячеслав')

    iterate_book()


def generate_agent_book(count_of_elements):
    if count_of_elements == '':
        count_of_elements = 10
    print(f'Generate random phone book with {count_of_elements} elements ...')
    def_date = date(year=1990, month=1, day=1)
    for i in range(int(count_of_elements)):
        rec = create_fake_record(def_date, i, book)
        book.add_record(rec)
        print(rec)


def iterate_book():
    print(f'Iterate AgentBook items:')
    for i, record in enumerate(AgentBookIterator(book)):
        print(f'{i}: {record}')


def paginate_book(count_of_elements = 3):
    # Iterate by 3 items per page
    print(f'\nIterate by {count_of_elements} items per page:')
    for i, records in enumerate(PaginatedAgentBookIterator(book, count_of_elements)):
        print(f"Portion {i + 1}: ")
        for pi in range(len(records)):
            print(f"{records[pi]}")


def create_fake_record(def_date, i, book: AgentBook = None):
    country = choice(['Україна', 'USA'])
    temp_fake = Faker('uk_UA') if country == 'Україна' else Faker('en_US')
    call_sign = temp_fake.first_name_female() if i % 2 else temp_fake.first_name_male()
    if book:
        try:
            book.find_record(call_sign)
            call_sign = f'{call_sign}{call_sign[-1]}'
        except CallSignNotFoundException:
            pass
    rec = Record(call_sign)
    if choice([True, False]):
        birth = def_date + timedelta(days=i)
        rec.birthday = birth.strftime(DATE_FORMAT)
    if choice([True, False]):
        rec.email = temp_fake.email()
    rec.add_phone(str(randint(1000000000, 9999999999)))
    if choice([True, False]):
        rec.add_phone(str(randint(1000000000, 9999999999)))
    if choice([True, False]):
        rec.address = Address(
            country,
            choice(UKRAINIAN_REGIONS) if country == 'Україна' else temp_fake.state(),
            temp_fake.city(),
            temp_fake.postcode() if country == 'Україна' else temp_fake.zipcode_plus4(),
            temp_fake.street_address()
        )
    return rec


if __name__ == '__main__':
    test_change_call_sign()
    generate_agent_book(100)
    paginate_book(12)