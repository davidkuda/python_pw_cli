import json
import string
import random
import datetime
from typing import Callable, List

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

    def remove_secrets_data(self, key: str, section: str = None):
        """Removes a password from the creds.json file."""
        section = section or 'main'
        self.pw_dict[section].pop(key)
        self.save_dict_to_file()
        print(f'Deleted {key} from {section}')
        print('')

    def find_key(self, search_term: str) -> List[dict]:
        """Iterate over all secrets and yield a secret's name that matches the search_term."""
        for section, secrets in self.pw_dict.items():
            for secret in secrets:
                if search_term.lower() in secret.lower():
                    yield {'entity': secret,
                           'section': section}

    # TODO: Move generate random pw to utils
    @staticmethod
    def generate_random_password(special_characters=True,
                                 password_length: int = 42) -> str:
        """Generates a random password and returns it as a string."""
        digits = string.digits
        letters = string.ascii_letters
        punctuation = r"!#$%&()*+:,-./;<=>?@[]^_{|}~" if special_characters else ''
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

    def get_sections(self) -> List[str]:
        """Get all sections of the secrets data file (json)."""
        return [pw for pw in self.pw_dict.keys()]

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

    def open_pw_file(pw_file_path, app: str = 'Sublime'):
        """Open pw file with an app (default: Sublime)."""
        raise NotImplementedError

