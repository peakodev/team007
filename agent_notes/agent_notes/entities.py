from collections import UserDict
from pathlib import Path
import copy
import pickle
import textwrap

HEADER = '\n{0:^5}| {1:^40}| {2:^20}\n{3:-^70s}'.format('id','note','tags','-')

def validate_note(value):
    if isinstance(value, str) and len(value) >= 3:
        return True

def wrap(string, width):
    #return textwrap.fill(string, width)
    return [string[i:i + width] for i in range(0, len(string), width)]

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class NoteID(Field):
    pass


class NoteText(Field):
    def __init__(self, value):
        if validate_note(value):
            super().__init__(value)
        else:
            raise ValueError('Note should have text')

class NoteTags(Field):
    def __init__(self, value):
        if validate_note(value):
            super().__init__(value)
        else:
            raise ValueError('Tag should have text')

class Note:
    def __init__(self, note_id, note_text: str, *tags: str):
        self.note_text = NoteText(note_text)
        self.note_id = NoteID(note_id)
        if tags:
            self.tags = [NoteTags(tag) for tag in tags]
        else:
            self.tags = []
    
    def add_tag(self, *tags):
        for tag in tags:
            if not any(obj.value == tag for obj in self.tags):
                tag_obj = NoteTags(tag)
                self.tags.append(tag_obj)
    
    def find_in_tag(self, string):
        for t in self.tags:
            if string in t.value:
                return ', '.join(t.value for t in self.tags)
    
    def find_in_text(self, string:str):
        if string in self.note_text.value:
            return self.note_text
    
    def remove_tag(self, tag):
        for t in self.tags:
            if tag == t.value:
                self.tags.remove(t)
            else:
                raise ValueError('Tag not found')

    def edit_tag(self, tag, new_tag):
        self.remove_tag(tag)
        self.add_tag(new_tag)

    def __str__(self):
        txt = wrap(self.note_text.value,38)
        list = ['\n{0:5}| {1:40}| {2:20}'.format('', txt[i],'') for i in range(len(txt))]
        #print(string)
        return '\x1b[31m{0:^5}\x1b[0m| {1:40}| \x1b[32m{2:20}\x1b[0m'.format(self.note_id.value, txt[0],', '.join(t.value for t in self.tags)) + \
               ''.join(list[1:]) + '\n{0:-^70s}'.format('-')
                  


class AgentNotes(UserDict):
    def __init__(self):
        super().__init__()
        p = Path(__file__)
        self.filename = p.parent / 'notes.pkl'

    def serialize(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def deserialize(self):
        try:
            with open(self.filename, "rb") as file:
                notes = pickle.load(file)
            return notes
        except FileNotFoundError:
            return self

    def add_note(self, note_text: str, *tags: str):
        self.data[len(self.data)+1] = Note(len(self.data)+1, note_text, *tags)
        self.serialize()
    
    def remove_note(self, id):
        self.data.pop(id)
        new_data = {}
        for note  in self.data.values():
            note.note_id.value = len(new_data)+1    # change id of note
            new_data[len(new_data)+1] = note        # change id in self.data.key
        self.data = copy.deepcopy(new_data)
        self.serialize()
    
    def edit_note(self, id, note, *tags):
        new_note = Note(id, note, *tags)
        self.data.update({id: new_note})
        self.serialize()

    def edit_note_tag(self, id, tag, *new_tag):
        self.data[id].edit_tag(tag, *new_tag)
        self.serialize()

    def add_note_tag(self, id, *new_tag):
        self.data[id].add_tag(*new_tag)
        self.serialize()
            
    def find_notes(self, text:str):
        print(HEADER)
        for note in self.data.values():
            tag_obj = note.find_in_tag(text)
            note_obj = note.find_in_text(text)
            if tag_obj:
                txt = wrap(note.note_text.value,30)
                list = ['\n{0:5}| {1:40}| {2:20}'.format('', txt[i],'') for i in range(len(txt))]
                t = tag_obj.partition(text)
                print('{0:^5}| {1:40}| {2:20}'.format(note.note_id.value, txt[0], '{0}\x1b[31m{1}\x1b[0m{2}'.format(t[0],t[1],t[2])) + ''.join(list[1:]) + '\n{0:-^70s}'.format('-'))
            elif note_obj:
                txt = wrap(note_obj.value,30)
                colored = []
                for item in txt:
                    n =  item.partition(text)
                    colored.append('{0}\x1b[31m{1}\x1b[0m{2}'.format(n[0],n[1],n[2]))
                list = ['\n{0:5}| {1:40}| {2:20}'.format('', colored[i],'') for i in range(len(colored))]               
                print('{0:^5}| {1:40}| {2:20}'.format(note.note_id.value, colored[0], ', '.join(t.value for t in note.tags)) + ''.join(list[1:]) + '\n{0:-^70s}'.format('-'))
        
    def show_all_notes(self):
        print(HEADER)
        for note in self.data.values():
            print(note)
    

    
