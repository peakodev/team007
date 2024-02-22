from agent_notes.test_notes import generate_notes
from agent_notes import AgentNotes
from agent_book import AgentBook, AgentBookIterator, ComingUpBirthdayAgentBookIterator
from prompt_toolkit import prompt
from toolbar import style, bottom_toolbar, rprompt
from completer import completer, completer_books

from colorama import init
init()
from colorama import Fore, Back, Style

book = AgentBook()

def show_help():  # separated help command for different modes
    available_commands = {
        'add note': "add new note , you can specify tags with #",
        'show notes all': "display all notes",
        'note add tag': 'add a tag to existing note by id',
        'edit note': 'edit existing note by id',
        'remove note': "remove existing note by id",
        'find notes': 'find notes by any matches in text or id',
        'exit': "for exit",
        'help': "show help",
        
        'add': "Add a user to the phone book",   # 22.02.24
        'usr_del': "Delete a user from the phone book",
        'phone_add': 'Add a phone number to the user',
        'email': 'Specify Email address',
        'del_phone': 'Remove a user''s phone number',
        'get_phone': 'Find out the user''s phone number',
        'upd_phone': 'Change phone number',
        'show_all': 'Get information from the entire phone book',
        'user_del': 'Delete a contact from the phone book',
        'birthday': 'Specify the user''s birthday',
        'bday': 'Find out how many days your birthday is in',
        'find': 'Find contacts falling within a specified interval',
    }
    available_commands_book = {
        'contact': 'Add a new contact',
        'change contact': 'Change contact name',
        'delete': 'remove contact by name',
        'target': 'Find contact',
        'all targets': 'List all contacts',
        'coming targets': 'Show contact with birthday in next week or specified number of days'
    }
    available_commands_xfiles = {
        'organize files': 'organize files',
        'exit': "for exit",
        'help': "show help"

    }
    if Bot().mode == '1':
        for key, description in available_commands_book.items():
            print("{:<20} -> {:>}".format(key, description))
    if Bot().mode == '2':
        for key, description in available_commands.items():
            print("{:<20} -> {:>}".format(key, description))


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Bot:
    def __init__(self):
        self.__isRunning = True
        self.__book = None
        self.__notes = None
        self.__mode = None
        self.__commands = dict()

    @property
    def running(self):
        return self.__isRunning

    @running.setter
    def running(self, value):
        self.__isRunning = value

    @property
    def notes(self):  # deserialize notes
        if self.__notes is None:
            self.__notes = AgentNotes().deserialize()
        return self.__notes

    @property
    def book(self) -> AgentBook:
        if self.__book is None:
            self.__book = AgentBook().deserialize()
        return self.__book

    @property
    def commands(self) -> dict:
        return self.__commands

    @commands.setter
    def commands(self, commands: dict):
        self.__commands = commands

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    def iterate_book(self):
        for i, record in enumerate(AgentBookIterator(self.book)):
            # print(f'{i}: {record}')
            print("{:<3}|{}".format(i, record))
            print("___|__")

    def birthday_iterate_book(self, days: int = 7):
        print(f'Targets in next {days} days:')
        for i, record in enumerate(ComingUpBirthdayAgentBookIterator(self.book, days)):
            print(f'{i}: {record}')

    def change_mode(self):
        print("Please select:\n")
        print("1. Work with Contacts book")
        print("2. Work with Notes")
        print("3. Exit")
        try:
            mode = prompt('>>')
            if mode in ['1', '2']:
                self.mode = mode
        except Exception as e:
            print(e)


def bot_exit():
    print("Good bye")
    Bot().notes.serialize
    Bot().book.serialize
    Bot().running = False
    
'''---------------- 22.02.24 -----------------'''    
def check_param(num_of_param, plus='+'):
    
    def check(func):
        if num_of_param >= 10:
            beg = num_of_param // 10
            end = num_of_param % 10
        else:
            beg = num_of_param
            end = beg
            
        def wrapper(*arg):
            param  = tuple(filter(lambda x: x, ' '.join(arg).split(' ')))
            if len(param) < beg or len(param) > end:
                raise ValueError(Fore.LIGHTRED_EX + 'Помилка у кількості параметрів ' + Fore.LIGHTBLUE_EX + \
                    f'Очікувалося {beg} отримано {len(param)}') 

            record = None
            if plus == '+':
                record = book.find_record(param[0])
                if record == None:
                    raise ValueError('Користувач '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RED+\
                        "відсутній в телефонній книзі")

            return func(param, record)
            
        return wrapper
    
    return check

@check_param(24, '-')
def add_user(param, empty):
    name_user = param[0]
    num_phone = param[1]
    if len(param) == 3:
        birthday = param[2].replace('.', '-')
    else:
        birthday = None
        
    book.add(name_user, num_phone, birthday)
    return 'Користувач '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+' додан до телефонної книги'
    
@check_param(1)
def del_user(param, empty):
    book.delete(param[0])
    return 'Користувач '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
           ' вилучен з телефонної книги '

@check_param(3) 
def change_phone(param, record):
    record.edit_phone(param[1], param[2])
    return 'Користувачеві '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
           ' телефонний номер '+Fore.LIGHTBLUE_EX+f' {param[1]} '+Fore.RESET+\
           ' замінено на '+Fore.LIGHTBLUE_EX+f' {param[2]} '+Fore.RESET
    
    
@check_param(2)
def add_phone(param, record):
    record.add_phone(param[1])
    return f'Телефонний номер '+Fore.LIGHTBLUE_EX+f' {param[1]} '+Fore.RESET+\
        ' доданий користувачеві '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET

@check_param(2)
def del_phone(param, record):
    record.remove_phone(param[1])
    return f'Телефонний номер '+Fore.LIGHTBLUE_EX+f'{param[1]}'+Fore.RESET+\
            ' вилучено у користувача '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET
    
@check_param(2)
def add_birthday(param, record):
    book.add_birthday(param[0], param[1].replace('.', '-'))
    return 'Користувачеві '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
           ' встановлено день народження '+Fore.LIGHTBLUE_EX+f' {param[1]} '+Fore.RESET
    
@check_param(2)
def add_email(param, record):
    book.add_email(param[0], param[1].replace('.', '-'))
    return 'Користувачеві '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
           ' встановлено Emall '+Fore.LIGHTBLUE_EX+f' {param[1]} '+Fore.RESET
    
@check_param(1)
def next_birthday(param, record):
    next_day = record.days_to_birthday()
    return 'У користувача '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
        ' день народження через '+Fore.LIGHTBLUE_EX+f' {next_day} днів'+Fore.RESET

@check_param(1,'-')
def find_users(param, record):
    list_user = book.find(param[0])
    if len(list_user) == 0:
       return Fore.LIGHTYELLOW_EX+'Користувачів із зазначеними параметрами не знайдено'
    
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + '\n\n')    
    for name_user in list_user:
        print(name_user)
    print(Fore.RESET + Style.RESET_ALL + '\n')    
    
'''----- Не доработано ----------------------------------------------------------------'''    
def show_all():
    ''' Друк інформації про всіх користувачів'''
    pass    
    
@check_param(1)
def find_phone(param, record):
    phone = record.find_phone(param[0])        # Не понятна работа !!!!!!!!!!! 
    return phone
'''-------------------------------------------------------------------------------------'''    




def input_handler(input_string):
    # separated = input_string.split()
    entered_command = ''
    for i in input_string:
        entered_command += ''.join(i)
        # print(entered_command)
        if entered_command in Bot().commands.keys():
            return entered_command, input_string[len(entered_command):].strip()
    raise ValueError


def command_handler(command, input_string):
    user_command = Bot().commands.get(command)
    if input_string:
        text, *tag = input_string.strip().split('--')
        ids = None
        if text.strip().split(' ', 1)[0].isdigit():
            ids, *text = text.strip().split(' ', 1)  # Does not pars tags for edit note
            user_command(ids, *text)
            return
        user_command(text, *tag)
    else:
        user_command()


def book_command_handler(command, input_string):
    user_command = Bot().commands.get(command)
    if input_string:
        return user_command(*input_string.strip().split(' '))
    else:
        return user_command()


# def get_agent_book():
#     for record in AgentBookIterator(Bot().book):
#         print(str(record))
#
#
# def get_agent_book_birthday(days=1):
#     for record in ComingUpBirthdayAgentBookIterator(Bot().book, after_days=days):
#         print(str(record))


def bot_start():
    bot = Bot()
    # COMMANDS = {
    #     'add agent': bot.book.add,
    #     'remove agent': bot.book.delete,
    #     'find agent': bot.book.find,
    #     'find agent phones': bot.book.get_phones,
    #     'show agents all': get_agent_book,
    #     'show agents birthday': get_agent_book_birthday,
    #     'add note': bot.notes.add_note,
    #     'exit': bot_exit,
    #     'show notes all': bot.notes.show_all_notes,
    #     'note add tag': bot.notes.add_note_tag,
    #     'edit note': bot.notes.edit_note,
    #     'remove note': bot.notes.remove_note,
    #     'find notes': bot.notes.find_notes,
    #     'organize files': organize_files,
    #     'help': show_help,
    #     'generate notes': generate_notes
    # }
    COMMANDS = {
        'help': show_help,
        'exit': bot_exit,
        'return': bot.change_mode,
        
        'add': add_user,   # 22.02.24
        'usr_del': del_user,
        'phone_add': add_phone,
        'del_phone': del_phone,
        'get_phone': find_phone,
        'upd_phone': change_phone,
        'show_all': show_all,
        'user_del': del_user,
        'birthday': add_birthday,
        'email': add_email,
        'bday': next_birthday,
        'find': find_users,
        
        'wrong command': None,
        'add note': bot.notes.add_note,
        'show notes all': bot.notes.show_all_notes,
        'note add tag': bot.notes.add_note_tag,
        'edit note': bot.notes.edit_note,
        'remove note': bot.notes.remove_note,
        'find notes': bot.notes.find_notes,
        'generate notes': generate_notes,

        'contact': bot.book.add,
        'change contact': bot.book.change_call_sign,
        'delete': bot.book.delete,
        'target': bot.book.find_record,
        'all targets': bot.iterate_book,
        'coming targets': bot.birthday_iterate_book

    }
    bot.commands = COMMANDS
    bot.change_mode()  # Asking user to choose mode
    while bot.running:
        if bot.mode == '2':  # Notes loop
            try:
                user_input = prompt(">>", completer=completer, bottom_toolbar=bottom_toolbar)  # Removed right toolbar
                user_command, input_string = input_handler(str(user_input))
                # print(len(input_string))
                command_handler(user_command, input_string)
            except Exception as e:
                print(e)
        elif bot.mode == '1':  # Books loop
            try:
                user_input = prompt(">>", completer=completer_books)
                user_command, input_string = input_handler(str(user_input))
                # print('You entered command:', user_command, "with such params", input_string)
                result = book_command_handler(user_command, input_string)
                if result:
                    print(result)

            except Exception as e:
                print(e)
        elif bot.mode == '3':
            bot_exit()
        else:
            bot.change_mode()

if __name__ == "__main__":
    bot_start()
