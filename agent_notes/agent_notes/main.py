from collections import UserDict
from pathlib import Path
import copy
import pickle


class Colour:
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   RED = '\033[91m'
   END = '\033[0m'


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class NoteText(Field):
    def __init__(self, value):
        if len(value) >= 5:
            super().__init__(value)
        else:
            raise ValueError('Note should have text')


class NoteTags(Field):
    pass


class Note:
    def __init__(self, note_text: str, *tags: str):
        self.note_text = NoteText(note_text)
        if tags:
            self.tags = [NoteTags(tag) for tag in tags]
        else:
            self.tags = []
    
    def add_tag(self, *tags):
        for tag in tags:
            tag_obj = NoteTags(tag)
            self.tags.append(tag_obj)
    
    def find_tag(self, tag):
        for t in self.tags:
            if t.value == tag:
                return t
    
    def remove_tag(self, tag):
        tag_obj = self.find_tag(tag)
        if tag_obj:
            self.tags.remove(tag_obj)
        else:
            raise ValueError('Tag not found')

    def edit_tag(self, tag, new_tag):
        self.remove_tag(tag)
        self.add_tag(new_tag)
    
    #def __str__(self):
    #    return f"{self.note_text.value}\nTags: {', '.join(t.value for t in self.tags)}\n"


class NotesBook(UserDict):
    def __init__(self):
        super().__init__()
        p = Path(__file__)
        self.filename = p.parent / 'notes.pkl'

    def serialize(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def deserialize(self):
        with open(self.filename, "rb") as file:
            notes = pickle.load(file)
        return notes

    def add_note(self, note):
        self.data[len(self.data)+1] = note
    
    def remove_note(self, id):
        self.data.pop(id)
        new_data = {}
        for note in self.data.values():
            new_data[len(new_data)+1] = note
        self.data = copy.deepcopy(new_data)
    
    def edit_note(self, id, note, *tags):
        new_note = Note(note, *tags)
        self.data.update({id: new_note})

    def edit_note_tag(self, id, tag, new_tag):
        self.data[id].edit_tag(tag, new_tag)
            
    def find_notes(self, tag):
        print('\n{0:^5}|{1:^40}|{2:^20}\n{3:-^70s}'.format('id','note','tags','-'))
        for id,note in self.data.items():
            tag_obj = note.find_tag(tag)
            if tag_obj:
                print('{0:^5}| {1:<39}| \x1b[32m{2:<20}\x1b[0m'.format(id, note.note_text.value,', '.join(t.value for t in note.tags if t == tag_obj)))  
        
    def show_notes(self):
        print('\n{0:^5}|{1:^40}|{2:^20}\n{3:-^70s}'.format('id','note','tags','-'))
        for id,note in self.data.items():
            print('{0:^5}| {1:<39}| {2:<20}'.format(id, note.note_text.value,', '.join(t.value for t in note.tags)))

    
notes1 = NotesBook()
note1 = Note('buy bread, appels, milk', 'shop')
note2 = Note('car vin number SB1KZ28E70E058799')
note2.add_tag('vin', 'car')
note3 = Note('wifi password hackme1234')
note3.add_tag('password', 'wifi', 'home')

notes1.add_note(note1)
notes1.add_note(note2)
notes1.add_note(note3)
notes1.serialize()

notes2 = NotesBook().deserialize()
print('\nshow deserialized notes')
notes2.show_notes()
notes2.add_note(Note('15600 x 8750','home','size'))
print('\nadding new note')
notes2.show_notes()
print('\nfind note by tag "home"')
notes2.find_notes('home')
print('\nremove note by id')
notes2.remove_note(2)
notes2.show_notes()
print('\nedit note and note tag')
notes2.edit_note(2,'wifi password 12345678', 'password', 'wifi')
notes2.edit_note_tag(2, 'wifi', 'fiwi')
notes2.show_notes()
