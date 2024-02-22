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
    'show_all': None,
    'add_note': None,
    'edit_note': None,
    'remove_note': None,
    'find_notes': None,
    'add_tag':None,
    'help': None,
    'exit': None,
    'generate': None,
    'return': None
})
completer_books = NestedCompleter.from_nested_dict({  # autocompleter for Contacts books mode
    'add': None,  # 22.02.24
    'usr_del': None,
    'phone_add': None,
    'del_phone': None,
    'get_phone': None,
    'upd_phone': None,
    'show_all': None,
    'user_del': None,
    'birthday': None,
    'email': None,
    'bday': None,
    'find': None,
    'exit': None,
    'return': None
})
completer_files = NestedCompleter.from_nested_dict({  # autocompleter for Contacts books mode
    'organize_files': None,
    'exit': None,
    'help': None,
    'return': None
})