import json
import os
from datetime import datetime
from GptMessage import GptMessage


class GptFile:
    def __init__(self):
        self.filename = None
        self.messages = []
        self.modified = False
        self.base_path = os.path.expanduser('~/.gpt')
        os.makedirs(self.base_path, exist_ok=True)

    @property
    def buffer_path(self):
        return os.path.join(self.base_path, ".buffer.json")

    def save_buffer(self):
        with open(self.buffer_path, 'w') as f:
            json.dump({
                'filename': self.filename,
                'messages': [{'role': m.role, 'content': m.content} for m in self.messages],
                'modified': self.modified
            }, f, indent=2)

    @classmethod
    def load_buffer(cls):
        file = cls()
        if not os.path.exists(file.buffer_path):
            return file
        with open(file.buffer_path, 'r') as f:
            data = json.load(f)
        file.filename = data['filename']
        file.messages = [GptMessage(**m) for m in data['messages']]
        file.modified = data['modified']
        modified_time = datetime.fromtimestamp(os.path.getmtime(file.buffer_path))
        GptMessage.app_message(f"Loaded from buffer (last modified: {modified_time})")
        if file.filename:
            GptMessage.app_message(f"Filename: {file.filename}")
        for msg in file.messages:
            msg.print()
        return file

    def save(self):
        if not self.messages:
            GptMessage.app_message("Buffer is empty, nothing to save", error=True)
            return

        while not self.filename:
            filename = input("Enter a filename to save to: ")
            if not filename:
                GptMessage.app_message("Filename cannot be empty", error=True)
                continue
            if filename.startswith('.'):
                GptMessage.app_message("Filename cannot start with a dot", error=True)
                continue
            self.filename = os.path.join(self.base_path, filename)
            if os.path.exists(self.filename):
                GptMessage.app_message("File already exists, choose another filename", error=True)
                self.filename = None

            if not self.filename.endswith('.json'):
                self.filename += '.json'

        path = os.path.join(self.base_path, self.filename)
        with open(path, 'w') as f:
            json.dump({
                'filename': self.filename,
                'messages': [{'role': m.role, 'content': m.content} for m in self.messages],
                'modified': false
            }, f, indent=2)
        self.save_buffer()
        GptMessage.app_message(f"History saved to {path}")
        self.modified = False

    def append(self, message):
        self.messages.append(message)
        self.modified = True
        self.save_buffer()

    def clear(self):
        self.messages.clear()
        self.modified = False
        self.filename = None
        self.save_buffer()
        GptMessage.app_message("Buffer cleared")
