# from agent_book.agent_book.entities import AgentBook
from entities import AgentBook
from prompt_toolkit import prompt
from toolbar import style, bottom_toolbar, rprompt
from completer import completer
from colorama import init
init()
from colorama import Fore, Back, Style


book = AgentBook()
 
def show_help():
    available_commands = {
        'hello': "say hello",
        'add': "add contact, example add john 1234567890",
        'add_phone': "Add a phone number, example add_phone john 1234567890",
        'del_phone': "Delete phone number, example del_phone john 1234567890",
        'change': 'change number in existing contact. example: change John old_phone new_phone',
        'phone': "find contact by name. example: phone John",
        'show_all': "returns all contacts in book",
        'delete': "remove contact from the book, example: delete john",
        'birthday': "set a birthday for contact, example: birthday john 2022-11-11",
        'bday': 'return days till next birthday of a contact, example: bday john',
        'find': 'find any matches in contact name or phones, example: find xxx'
    }
    for key, description in available_commands.items():
        print("{:<10} -> {}".format(key, description))


def check_param(num_of_param, plus='+'):
    
    def check(func):
        if num_of_param >= 10:
            beg = num_of_param // 10
            end = num_of_param % 10
        else:
            beg = num_of_param
            end = beg
            
        def wrapper(*arg):
            param  = tuple(filter(lambda x: x, ''.join(arg).split(' ')))
            if len(param) != beg and len(param) != end:
                raise ValueError('Error: Invalid number of parameters. ' + Fore.LIGHTBLUE_EX + \
                    f'Expected {beg} received {len(param)}' + Fore.RESET) 

            record = None
            if plus == '+':
                record = book.find_record(param[0])
                if record == None:
                    raise ValueError('User '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RED+\
                        ' is not in the phone book')
                
            return func(param, record)
            
        return wrapper
    
    return check

@check_param(23, '-')
def add_user(param, empty):
    name_user = param[0]
    num_phone = param[1]
    if len(param) == 3:
        birthday = param[2].replace('.', '-')
    else:
        birthday = None
        
    book.add(name_user, num_phone, birthday)
    return 'User '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+' added to phone book'
    
@check_param(1, '-')
def del_user(param, empty):
    book.delete(param[0])
    return 'User '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
           ' has been removed from the phone book '

@check_param(3) 
def change_phone(param, record):
    record.edit_phone(param[1], param[2])
    return 'User '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
           ' phone number '+Fore.LIGHTBLUE_EX+f' {param[1]} '+Fore.RESET+\
            ' replaced with '+Fore.LIGHTBLUE_EX+f' {param[2]} '+Fore.RESET
    
    
@check_param(2)
def add_phone(param, record):
    record.add_phone(param[1])
    return f'Phone number '+Fore.LIGHTBLUE_EX+f' {param[1]} '+Fore.RESET+\
        ' has been added to user '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET

@check_param(2)
def add_birthday(param, record):
    record.add_birthday(param[1].replace('.', '-'))
    return 'User '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
           ' has a birthday recorded '+Fore.LIGHTBLUE_EX+f' {param[1]} '+Fore.RESET
    
@check_param(2)
def del_phone(param, record):
    record.remove_phone(param[1])
    return f'Phone number '+Fore.LIGHTBLUE_EX+f'{param[1]}'+Fore.RESET+\
            ' has been deleted for user '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET
    
    
@check_param(1)
def find_phone(param, record):
    phone = record.find_phone(param[0])        # Не понятна работа !!!!!!!!!!! 
    return phone

@check_param(1)
def next_birthday(param, record):
    next_day = record.days_to_birthday()
    return 'User '+Fore.LIGHTBLUE_EX+f' {param[0]} '+Fore.RESET+\
        ' has a birthday in '+Fore.LIGHTBLUE_EX+f'{next_day} days'+Fore.RESET

@check_param(1,'-')
def find_users(param, record):
    list_user = book.find(param[0])
    if len(list_user) == 0:
       return Fore.LIGHTYELLOW_EX+'Users with the specified parameters were not found'
        
    for name_user in list_user:
        print(name_user)
    

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
        self.__commands = dict()

    @property
    def running(self):
        return self.__isRunning

    @running.setter
    def running(self, value):
        self.__isRunning = value

    def notes(self):  # deserialize notes
        pass
    
    @property
    def commands(self) -> dict:
        return self.__commands

    @commands.setter
    def commands(self, commands: dict):
        self.__commands = commands

    @property
    def note(self):
        pass

    @note.setter
    def note(self, id):
        pass

def bot_exit():
    print("Good bay")
    Bot().running = False


def input_handler(input_string):
    separated = input_string.split()
    for i in separated:
        entered_command = ''.join(i)
        if entered_command in Bot().commands.keys():
            return entered_command, input_string[len(entered_command):]
    raise ValueError('Error. Wrong command')


def command_handler(command, input_string: str):
    user_command = Bot().commands.get(command)
    return user_command(*input_string)

def bot_start():
    bot = Bot()
    COMMANDS = {
        'add': add_user,
        'add_phone': add_phone,
        'del_phone': del_phone,
        'exit': bot_exit,
        'change': change_phone,
        'phone': find_phone,
        'show_all': None,
        'wrong command': None,
        'delete': del_user,
        'birthday': add_birthday,
        'bday': next_birthday,
        'find': find_users,
        'help': show_help
    }
    bot.commands = COMMANDS
    while bot.running:
        try:
            user_input = prompt(">>",completer=completer, bottom_toolbar=bottom_toolbar, style=style, rprompt=rprompt)
            # print(user_input)
            user_command, input_string = input_handler(str(user_input))
            txt_msg = command_handler(user_command, input_string)
            if txt_msg != None:
                print(Style.BRIGHT+Fore.LIGHTWHITE_EX + '\n' + txt_msg + Fore.RESET+Style.RESET_ALL)
                
        except ValueError as error_msg:
            print(Fore.LIGHTRED_EX + error_msg.args[0] + Fore.RESET)



if __name__ == "__main__":
    bot_start()
