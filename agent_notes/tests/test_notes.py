#import sys
#sys.path.insert(1,'C:\\Work\\team007\\team007\\agent_notes')

from agent_notes import AgentNotes
from agent_notes import PaginatedAgentNotesIterator

notes1 = AgentNotes()

notes1.add_note('Ненавижу чай. Это же просто грязная жижа. Больше того, чай — одна из главных причин падения Британской империи.', 'чай', 'причина')
notes1.add_note('Я обычно замечаю всякие мелочи — например, блондинка девушка или брюнетка.', 'мелочи', 'блондинка')
notes1.add_note('Почему люди, которые не слушают чужих советов, так любят давать собственные?', 'советы', 'люди')
notes1.add_note('Власть меняется — ложь остается.', 'власть', 'ложь')
notes1.add_note('Ради женщины с ножом я готов на все.', 'женщина', 'нож')

notes1.show_all_notes()
notes1.serialize()

notes2 = AgentNotes().deserialize()
print('\nshow deserialized notes')
notes2.show_all_notes()

print('\nremove note by id 4')
notes2.remove_note('4')
notes2.show_all_notes()

print('\nadd note without tag')
notes2.add_note('Власть меняется — ложь остается.')
notes2.show_all_notes()

print('\nadding tags to note, one wrong')
notes2.add_note_tag('5', 'jhjhgg', 'ложь')
notes2.show_all_notes()

print('\nedit note 5 tag')
notes2.edit_note_tag('5', 'jhjhgg', 'власть')
notes2.show_all_notes()

print('\nedit note 4 text and tag')
notes2.edit_note('4', 'Ради девушки с ножом я готов на все.', 'девушка', 'нож')
notes2.show_all_notes()

print('\nprint 2 items per page:')
for pages in PaginatedAgentNotesIterator(notes2,2):
    for item in pages:
        print(item)

print('\nfind note by tag "девушка"')
notes2.find_notes('девушка')

