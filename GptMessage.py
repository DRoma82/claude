from termcolor import colored


class GptMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def print_header(self):
        color = 'green' if self.role == 'human' else 'cyan'
        role_display = 'YOU' if self.role == 'human' else self.role.upper()
        print(colored(f'[{role_display}]:', color), end='')

    def print(self):
        self.print_header()
        if not self.content.endswith('\n'):
            print()

    @staticmethod
    def prompt():
        print(colored('YOU: ', 'green'), end='')

    @staticmethod
    def app_message(content, error=False, newline=True):
        color = 'red' if error else 'yellow'
        print(colored(f'[APP]: {content}', color), end='')
        if newline:
            print()
