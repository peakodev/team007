from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'rprompt': 'bg:#ff0066 #ffffff',
})


def rprompt():
    return """Total Contacts: 0 
              Total Notes 0"""


def bottom_toolbar():
    return f"Total Contacts:  Total Notes:  "

# text = prompt('> ', bottom_toolbar=bottom_toolbar)
# print('You said: %s' % text)
