from prompt_toolkit.completion import NestedCompleter

# completer = NestedCompleter.from_nested_dict({
#     'show': {'notes': {'all': None}, 'agents': {'all': None, 'birthday': None}},
#     'note': {'add': None},
#     'agent': {'add': None},
#     'add': {'note': None, 'agent': None},
#     'edit': {'note': None, 'agent': {'call-sign': None}},
#     'remove': {'note': None, 'agent': None},
#     'find': {'notes': None, 'agent': {'phones': None}},
#     'organize': {'files': None},
#     'help': None,
#     'exit': None,
# })

completer = NestedCompleter.from_nested_dict({  # autocompleter for Notes mode
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
completer_books = NestedCompleter.from_nested_dict({  # autocompleter for Contacts books mode
    'contact': None,
    'change': {'contact': None},
    'delete': None,
    'target': None,
    'all': {'targets': None},
    'coming': {'targets': None},
    'exit': None,
    'return': None
})