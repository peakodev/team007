from faker import Faker
from random import randint, choice
from datetime import date, timedelta
from agent_book import AgentBook, Record, PaginatedAgentBookIterator, Address, DATE_FORMAT, UKRAINIAN_REGIONS

book = AgentBook()


def generate_agent_book(count_of_elements):
    if count_of_elements == '':
        count_of_elements = 10
    print(f'\nGenerate random phone book with {count_of_elements} elements ...')
    fake_us = Faker('en_US')
    fake_ua = Faker('uk_UA')
    # Prepare book
    def_date = date(year=1990, month=1, day=1)
    for i in range(int(count_of_elements)):
        country = choice(['Україна', 'USA'])
        temp_fake = fake_ua if country == 'Україна' else fake_us
        name = temp_fake.first_name_female() if i % 2 else temp_fake.first_name_male()
        if book.find_record(name) is not None:
            name = f'{name} {i}'
        rec = Record(f"{name}")
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
        book.add_record(rec)
        print(rec)

    # Iterate by 3 items per page
    print('\nIterate by 3 items per page:')
    for i, records in enumerate(PaginatedAgentBookIterator(book, 3)):
        print(f"Portion {i + 1}: ")
        for pi in range(len(records)):
            print(f"{records[pi]}")


if __name__ == '__main__':
    generate_agent_book(100)
