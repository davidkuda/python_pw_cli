import json
import string
import random
import datetime
from typing import Callable

import pw_utils


class PasswordClient:
    def __init__(self, creds_dir: str, creds_file_path: str):
        self.creds_dir = creds_dir
        self.creds_file_path = creds_file_path
        self.pw_dict = pw_utils.get_pws_from_json_file(creds_file_path)
        # TODO: Move crypto to the command

    def get_secrets_data(self, entity: str, section: str = None) -> dict:
        """Return secrets data from self.pw_dict.

        Args:
            entity (str):
                The name of the holder of the password, e.g. "GitHub".
            section (str, optional):
              Defaults to "main". Adjust if you want to access data from an
              other section.
        """
        if section is None:
            section = 'main'
        secrets_data = self.pw_dict[section][entity]
        return secrets_data

    # TODO: Move generate random pw to utils
    @staticmethod
    def generate_random_password(special_characters=True,
                                 password_length: int = 42) -> str:
        """Generates a random password and returns it as a string."""
        digits = string.digits
        letters = string.ascii_letters
        punctuation = r"!#$%&()*+:,-./;<=>?@[]^_{|}~" if special_characters else None
        characters = digits + letters + punctuation
        random_password = ''.join(random.choice(characters) for i in range(password_length))
        return random_password

    def add_new_secrets_data(self, entity: str, secrets_data: dict,
                             section: 'str' = None, overwrite: bool = False) -> bool:
        """Adds new secrets data to the password file.

        If the a password already exists in the creds.json file, this method will update it.

        Args:
            entity (str): The entity that you need the password for, e.g. "GitHub"
            secrets_data (dict):
                A dictionary that you want to store and that holds your
                secrets. Example:
                    {'password': 'p4ssw0rd',
                    'website': 'https://kuda.ai',
                    'user_name': 'DataDave'}
            section (str, optional):
                You may set the section of the json file to which this
                password will be added to. Defaults to the section "main".
            overwrite (bool, optional):
                If set to True, an existing password will be overwritten.

        Returns:
            bool: True for writing new data, False if no action.
        """
        self.create_backup()

        if section is None:
            section = 'main'

        if not self.check_existence_of_section(section):
            self.create_section(section)

        if entity in self.pw_dict[section] and overwrite is False:
            print('Entity is already there. Nothing happened.')
            print('Use the -ow / --overwrite option to update existing secrets data.')
            return False

        new_secrets_data = {entity: secrets_data}

        print(f'Created new password for "{entity}".')
        print('')

        self.pw_dict[section].update(new_secrets_data)
        self.save_dict_to_file()
        return True

    def create_backup(self):
        """Create a backup of the dictionary with the passwords."""
        now = datetime.datetime.now().isoformat()
        pretty_now = now.split('.')[0].replace(':', '.')
        with open(f'{self.creds_dir}/.backups/{pretty_now}', 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

    def save_dict_to_file(self):
        with open(self.creds_file_path, 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

    def create_section(self, section_name: str) -> None:
        """Creates a new section."""
        if self.check_existence_of_section(section_name):
            return print(f'Section {section_name} exists already.')
        self.pw_dict[section_name] = {}
        self.save_dict_to_file()
        print(f'Created a new section: "{section_name}".')

    def print_sections(self):
        """Print all keys of a dictionary (depth -> 1)."""
        for key in self.pw_dict.keys():
            print(key)

    def print_keys_of_section(self, section_name):
        """Output all available keys of a section to the console."""
        for key in self.pw_dict[section_name].keys():
            print(key)

    def check_existence_of_section(self, section: str):
        if section in self.pw_dict:
            return True

    def remove_section(self, section):
        self.pw_dict.pop(section)
        self.save_dict_to_file()
        print(f'Removed Section: "{section}"')

    def remove_entity(self, entity: str, section: str = None) -> None:
        """Removes a password from the creds.json file."""
        section = section or 'main'
        self.pw_dict[section].pop(entity)
        self.save_dict_to_file()
        print(f'Deleted {entity} from {section}')
        print('')

    def open_pw_file(pw_file_path, app: str = 'Sublime'):
        """Open pw file with an app (default: Sublime)."""
        raise NotImplementedError

    def manipulate_passwords(self, crypto: Callable = None) -> None:
        """Iterate over all passwords and manipulate them.

        You can apply encryption or decryption by passing the corresponding
         processor as an argument.

        Args:
            crypto (Callable): Pass for instance "self.crypto.encrypt" to
              encrypt all passwords.
        """
        for section, entities in self.pw_dict.items():
            for entity, v in entities.items():
                current_password = v.get("password")
                manipulated_password = crypto(current_password)
                v["password"] = manipulated_password
        self.save_dict_to_file()
