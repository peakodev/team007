#from prompt_toolkit import prompt   #just for test can be removed later
from prompt_toolkit.completion import NestedCompleter

completer = NestedCompleter.from_nested_dict({
    'show': {'all'},
    'hello': None,
    'add': None,
    'add_phone': None,
    'del_phone': None,
    'birthday': None,
    'bday': None,
    'change': None,
    'phone': None,
    'delete': None,
    'find': None,
    'help': None,
    'exit': None,
})

#text = prompt('# ', completer=completer) # #just for test can be removed later
#print('You said: %s' % text)   #  #just for test can be removed later