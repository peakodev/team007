#from prompt_toolkit import prompt   #just for test can be removed later
from prompt_toolkit.completion import NestedCompleter

completer = NestedCompleter.from_nested_dict({
    'show': {'all'},
    'hello': None,
    'add': None,
    'change': None,
    'phone': None,
    'delete': None,
    'help': None,
    'exit': None,
})

#text = prompt('# ', completer=completer) # #just for test can be removed later
#print('You said: %s' % text)   #  #just for test can be removed later