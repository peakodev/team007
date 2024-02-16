from faker import Faker
from random import randint
from datetime import date, timedelta
from agent_book import AgentBook, Record, DATE_FORMAT, PaginatedAgentBookIterator

book = AgentBook()


def generate_agent_book(count_of_elements):
    if count_of_elements == '':
        count_of_elements = 10
    print(f'\nGenerate random phone book with {count_of_elements} elements ...')
    fake = Faker()
    # Prepare book
    def_date = date(year=1990, month=1, day=1)
    for i in range(int(count_of_elements)):
        birth = def_date + timedelta(days=i)
        name = fake.first_name_female() if i % 2 else fake.first_name_male()
        if book.find_record(name) is not None:
            name = f'{name} {i}'
        rec = Record(f"{name}", birth.strftime(DATE_FORMAT))
        rec.add_phone(str(randint(1000000000, 9999999999)))
        rec.add_phone(str(randint(1000000000, 9999999999)))
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
