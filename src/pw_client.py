import sys
import json
import string
import random
import datetime

import pyperclip

import pw_utils


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

    def get_pw(self, entity: str, attribute: str = None, section: str = None) -> None:
        """Get data from self.pw_dict, copy to clipboard and print to console.

        Args:
            entity (str): The name of the holder of the password, e.g. "GitHub".
            attribute (str, optional): Defaults to "password". Adjust if you want to retrieve "username" or "website".
            section (str, optional): Defaults to "main". Adjust if you want to access data from an other section.
        """
        if attribute is None:
            attribute = 'password'
        if section is None:
            section = 'main'

        pw_info = self.pw_dict[section][entity]
        pyperclip.copy(pw_info[attribute])

        print(f'Copied {attribute} for "{entity}" into your clipboard.')
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

    @staticmethod
    def copy_and_print_pw(pw):
        pyperclip.copy(pw)
        print('Here is your random password:')
        print(pw)
        print('It has been copied into your clipboard.')

    def save_dict_to_file(self):
        with open(self.creds_file_path, 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

    def add_new_pw(self, entity: str, password: str = None, username: str = None,
                   website: str = None, section: 'str' = None) -> None:
        """Adds a new password to the password file.

        If the a password already exists in the creds.json file, this method will update it.

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

        if section is None:
            section = 'main'

        if not self.check_existence_of_section(section):
            self.create_section(section)

        if password is None:
            password = self.generate_random_password()
        pyperclip.copy(password)

        new_password = {entity: {}}
        new_password[entity]['password'] = password
        new_password[entity]['username'] = username if username else 'not specified'
        new_password[entity]['website'] = website if website else 'not specified'

        print(f'Created new password for "{entity}".')
        print('Saved your new password to your creds file.')
        for k, v in new_password[entity].items():
            print(f'  {k}: {v}')
        print('')

        self.pw_dict[section].update(new_password)
        self.save_dict_to_file()

    def create_section(self, section_name: str) -> None:
        """Creates a new section."""
        if self.check_existence_of_section(section_name):
            return print(f'Section {section_name} exists already.')
        self.pw_dict[section_name] = {}
        self.save_dict_to_file()
        print(f'Created a new section: "{section_name}".')

    def check_existence_of_section(self, section: str):
        if section in self.pw_dict:
            return True

    def remove_section(self, section):
        self.pw_dict.pop(section)
        self.save_dict_to_file()
        print(f'Removed Section: "{section}"')

    def remove_password(self, entity: str, section: str = None) -> None:
        """Removes a password from the creds.json file."""
        section = section or 'main'
        self.pw_dict[section].pop(entity)
        self.save_dict_to_file()
        print(f'Deleted {entity} from {section}')
        print('')

    def open_pw_file(pw_file_path, app: str = 'Sublime'):
        """Open pw file with an app (default: Sublime)."""
        raise NotImplementedError

