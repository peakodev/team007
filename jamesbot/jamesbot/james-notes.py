# import agent_notes
from prompt_toolkit import prompt
from toolbar import style, bottom_toolbar, rprompt
from completer import completer


def show_help():
    available_commands = {
        'hello': "say hello",
        'add': "add contact, example add john 1234567890",
        'change': 'change number in existing contact. example: change John old_phone new_phone',
        'phone': "find contact by name. example: phone John",
        'show all': "returns all contacts in book",
        'delete': "remove contact from the book, example: delete john",
        'birthday': "set a birthday for contact, example: birthday john 2022-11-11",
        'bday': 'return days till next birthday of a contact, example: bday john',
        'find': 'find any matches in contact name or phones, example: find xxx'
    }
    for key, description in available_commands.items():
        print("{:<10} -> {}".format(key, description))


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
    raise ValueError


def command_handler(command, input_string):
    user_command = Bot().commands.get(command)
    user_command(*input_string)


def bot_start():
    bot = Bot()
    COMMANDS = {
        'add': bot.note,
        'exit': bot_exit,
        'change': None,
        'phone': None,
        'show all': None,
        'wrong command': None,
        'delete': None,
        'birthday': None,
        'bday': None,
        'find': None,
        'help': show_help
    }
    bot.commands = COMMANDS
    while bot.running:
        user_input = prompt(">>",completer=completer, bottom_toolbar=bottom_toolbar, style=style, rprompt=rprompt)
        print(user_input)
        user_command, input_string = input_handler(str(user_input))
        command_handler(user_command, input_string)


if __name__ == "__main__":
    bot_start()
