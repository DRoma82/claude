import re
from GptMessage import GptMessage


class Cmd:
    REGEX = re.compile(r'^:\w+!?$')

    def __init__(self, input):
        if not self.is_cmd(input):
            raise ValueError(f"Invalid command: {input}")

        self.is_force = input.endswith('!')
        self.name = input.lsrip(':').rstrip('!')

    @classmethod
    def is_cmd(cls, input):
        return bool(input) and bool(cls.REGEX.match(input))

    def _check_force(self, file):
        if self.is_force or not file.modified:
            return True

        GptMessage.app_message("Buffer has unsaved changes, use ! to force", error=True)
        return False

    def run(self, file):
        if self.name == 'b':
            if not self._check_force(file):
                return False
            file = GptFile.load_buffer()
            return False
        elif self.name == 'bd':
            if not self._check_force(file):
                return False
            file.clear()
            GptMessage.app_message("Buffer cleared")
            return False
        elif self.name == 'w':
            file.save()
            return False
        elif self.name == 'q':
            if not self._check_force(file):
                return False
            GptMessage.app_message("Goodbye!")
            return True
        elif self.name == 'wq':
            if not self._check_force(file):
                return False
            file.save()
            GptMessage.app_message("Goodbye!")
            return True
        else:
            GptMessage.app_message(f"Unknown command: {self.name}", error=True)
            return False
