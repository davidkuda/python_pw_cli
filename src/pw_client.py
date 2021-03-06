import pw_utils
import json
import string
import random
import datetime
import pyperclip
import sys


class PasswordClient:
    def __init__(self, creds_dir: str, creds_file_path: str):
        self.creds_dir = creds_dir
        self.creds_file_path = creds_file_path
        self.pw_dict = pw_utils.get_pws_from_json_file(creds_file_path)

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
        pw_info = self.pw_dict[section][pw_key]
        pyperclip.copy(pw_info['password'])

        print(f'Copied password for "{pw_key}" into your clipboard.')
        for k, v in pw_info.items():
            print(f'  {k}: {v}')
        print('')

    def create_backup(self):
        """Create a backup of the dictionary with the passwords."""
        now = datetime.datetime.now().isoformat()
        pretty_now = now.split('.')[0].replace(':', '.')
        with open(f'{self.creds_dir}/backups/{pretty_now}', 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

    @staticmethod
    def generate_random_password(special_characters=True):
        """Generates a random password with 42 characters of any type (letters, digits, special characters)."""
        digits = string.digits
        letters = string.ascii_letters
        punctuation = r"!#$%&()*+:,-./;<=>?@[]^_{|}~" if special_characters else None
        characters = digits + letters + punctuation
        random_password = ''.join(random.choice(characters) for i in range(42))
        return random_password

    def save_dict_to_file(self):
        with open(self.creds_file_path, 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

    def add_new_pw(self, entity: str, password: str = None, username: str = None,
                   website: str = None, section: 'str' = 'main') -> None:
        """Adds a new password to the password file.

        Args:
            entity (str): The entity that you need the password for, e.g. "GitHub"
            password (str, optional): If you want, you can specify a password. If you leave it,
              it will generate a random password with 42 characters.
            username (str, optional): Pass a user name if you want to add it to the json file.
            website (str, optional): Pass a website if you want to add it to the json file.
            section (str, optional): You may set the section of the json file to which this
              password will be added to. Defaults to the section "main".
        """
        self.create_backup()

        if password is None:
            password = self.generate_random_password()
        pyperclip.copy(password)

        new_password = {entity: {}}
        new_password[entity]['password'] = password
        new_password[entity]['username'] = username if username else 'not specified'
        new_password[entity]['website'] = website if website else 'not specified'

        print(f'Created new password for {entity}.')
        print('Saved your new password to your creds file.')
        for k, v in new_password[entity].items():
            print(f'  {k}: {v}')
        print('')

        self.pw_dict[section].update(new_password)
        self.save_dict_to_file()

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

