# from prompt_toolkit import prompt   #just for test can be removed later
from prompt_toolkit.completion import NestedCompleter

completer = NestedCompleter.from_nested_dict({
    'show': {'notes': {'all': None}, 'agents': {'all': None, 'birthday': None}},
    'note': {'add': None},
    'agent': {'add': None},
    'add': {'note': None, 'agent': None},
    'edit': {'note': None, 'agent': {'call-sign': None}},
    'remove': {'note': None, 'agent': None},
    'find': {'notes': None, 'agent': {'phones': None}},
    'help': None,
    'exit': None,
})

# text = prompt('# ', completer=completer) # #just for test can be removed later
# print('You said: %s' % text)   #  #just for test can be removed later
