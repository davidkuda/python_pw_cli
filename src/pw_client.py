import pw_utils
import json
import string
import random
import datetime
import pyperclip
import sys


class PasswordClient:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pw_dict = pw_utils.get_pws_from_json_file(file_path)

    def print_sections(self):
        """Print all keys of a dictionary (depth -> 1)."""
        for key in self.pw_dict.keys():
            print(key)

    def print_keys_of_section(self, section_name):
        """Output all available keys of a section to the console."""
        for key in self.pw_dict[section_name].keys():
            print(key)

    def get_pw(self, pw_key: str, section: str = 'main'):
        """Access a dictionary's data (pws[section][pw_key]) and copy value to clipboard."""
        pw = self.pw_dict[section][pw_key]['password']
        pyperclip.copy(pw)

    def create_backup(self):
        """Create a backup of the dictionary with the passwords."""
        now = datetime.datetime.now().isoformat()
        pretty_now = now.split('.')[0].replace(':', '.')
        with open(f'./backups/{pretty_now}', 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

    @staticmethod
    def generate_random_password():
        """Generates a random password with 42 characters of any type (letters, digits, special characters)."""
        characters = string.printable
        random_password = ''.join(random.choice(characters) for i in range(42))
        return random_password

    def add_new_pw(self, service: str, file_path: str, password: str = None, user_name: str = None,
                   website: str = None, section: 'str' = 'main') -> None:
        """Adds a new password to the password file."""

        self.create_backup()

        if password is None:
            password = self.generate_random_password()

        new_password = {service: {}}
        new_password[service]['password'] = password
        new_password[service]['user_name'] = user_name if user_name else 'not specified'
        new_password[service]['website'] = website if website else 'not specified'

        self.pw_dict.update(new_password)

        with open(file_path, 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

        @staticmethod
        def validate_user_input(args, num=1, response_msg='Pass an arg after pw'):
            """Validate if user has passed the correct number of args with the command."""
            try:
                args[num]
            except IndexError:
                sys.excepthook = pw_utils.my_exchandler
                raise IndexError(response_msg)
            else:
                pass

        def open_pw_file(pw_file_path, app: str = 'Sublime'):
            """Open pw file with an app (default: Sublime)."""
            pass

        def decrypt(pw_file_path):
            """Decrypt pw file."""
            pass

        def encrypt(pw_file_path):
            """Encrypt pw file."""
            pass

