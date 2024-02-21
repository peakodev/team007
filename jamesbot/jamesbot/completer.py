# from prompt_toolkit import prompt   #just for test can be removed later
from prompt_toolkit.completion import NestedCompleter

completer = NestedCompleter.from_nested_dict({
    'show': {'notes': {'all': None}},
    'note': {'add': None},
    'add': {'note': None},
    'edit': {'note': None},
    'remove': {'note': None},
    'find': {'notes': None},
    'help': None,
    'exit': None,
    'generate': None,
    'return': None
})
completer_books = NestedCompleter.from_nested_dict({
    'contact': None,
    'change': {'contact': None},
    'delete': None,
    'target': None,
    'all': {'targets': None},
    'coming': {'targets': None},
    'exit': None,
    'return': None
})
# text = prompt('# ', completer=completer) # #just for test can be removed later
# print('You said: %s' % text)   #  #just for test can be removed later
