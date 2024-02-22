from agent_notes.test_notes import generate_notes
from bot_class import Bot
from prompt_toolkit import prompt
from toolbar import style, bottom_toolbar, rprompt
from completer import completer, completer_books


def show_help():  # separated help command for different modes
    available_commands = {
        'add note': "add new note , you can specify tags with #",
        'show notes all': "display all notes",
        'note add tag': 'add a tag to existing note by id',
        'edit note': 'edit existing note by id',
        'remove note': "remove existing note by id",
        'find notes': 'find notes by any matches in text or id',
        'exit': "for exit",
        'help': "show help"
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


def bot_exit():
    print("Good bye")
    Bot().notes.serialize
    Bot().book.serialize
    Bot().running = False


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
                user_input = prompt(">>", completer=completer, bottom_toolbar=bottom_toolbar,rprompt=rprompt, style=style,
                                    complete_while_typing=True)  # Removed right toolbar
                user_command, input_string = input_handler(str(user_input))
                # print(len(input_string))
                command_handler(user_command, input_string)
            except Exception as e:
                print(e)
        elif bot.mode == '1':  # Books loop
            try:
                user_input = prompt(">>", completer=completer_books, bottom_toolbar=bottom_toolbar, style=style,
                                    complete_while_typing=True)
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
