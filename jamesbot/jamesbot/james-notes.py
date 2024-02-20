# from agent_notes import AgentNotes
from agent_notes import AgentNotes
from agent_book import AgentBook
from prompt_toolkit import prompt
from toolbar import style, bottom_toolbar, rprompt
from completer import completer

# MyBook = AgentBook().deserialize()
# MyBook.add("Orest")
# print(MyBook.find_record("Orest"))

def show_help():
    available_commands = {
        'add note': "add new note , you can specify tags with --",
        'show notes all': "display all notes",
        'note add tag': 'add a tag to existing note by id',
        'edit note': 'edit existing note by id',
        'remove note': "remove existing note by id",
        'find notes': 'find notes by any matches in text or id',
        'exit': "for exit",
        'help': "show help"
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

    @property
    def notes(self):  # deserialize notes
        if self.__notes is None:
            self.__notes = AgentNotes().deserialize()
        return self.__notes

    # # @property
    # def book(self) -> AgentBook:
    #     if self.__book is None:
    #         self.__book = AgentBook().deserialize()
    #     return self.__book

    @property
    def commands(self) -> dict:
        return self.__commands

    @commands.setter
    def commands(self, commands: dict):
        self.__commands = commands


def bot_exit():
    print("Good bay")
    Bot().notes.serialize
    Bot().running = False


def input_handler(input_string):
    # separated = input_string.split()
    entered_command = ''
    for i in input_string:
        entered_command += ''.join(i)
        #print(entered_command)
        if entered_command in Bot().commands.keys():
            return entered_command, input_string[len(entered_command):].strip()
    raise ValueError


def command_handler(command, input_string):
    user_command = Bot().commands.get(command)
    if input_string:
        text, *tag = input_string.strip().split('--')
        ids = None
        if text.strip().split(' ', 1)[0].isdigit():
            ids, *text = text.strip().split(' ', 1)         # Does not pars tags for edit note
            user_command(ids, *text)
            return
        user_command(text, *tag)
    else:
        user_command()


def bot_start():
    bot = Bot()
    COMMANDS = {
        'add note': bot.notes.add_note,
        'exit': bot_exit,
        'show notes all': bot.notes.show_all_notes,
        'note add tag': bot.notes.add_note_tag,
        'edit note': bot.notes.edit_note,
        'remove note': bot.notes.remove_note,
        'find notes': bot.notes.find_notes,
        'help': show_help,
        'generate_notes': bot.notes.generate_notes
    }
    bot.commands = COMMANDS
    while bot.running:
        try:
            user_input = prompt(">>", completer=completer, bottom_toolbar=bottom_toolbar, style=style, rprompt=rprompt)
            user_command, input_string = input_handler(str(user_input))
            #print(len(input_string))
            command_handler(user_command, input_string)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    bot_start()
