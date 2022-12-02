import sys
import argparse
from pprint import pprint
from typing import List

import pyperclip

from pw.pw_config import PWConfig, get_prod_config
from .pw_json_client import SecretsDataJSONClient
from .pw_utils import generate_random_password, find_key, HelpTexts as h
from crypto.synchronous_encryption_fernet import SynchronousEncryptionFernet


class PasswordCommand:
    def __init__(self, pw_config: PWConfig = None):
        if pw_config is None:
            pw_config = get_prod_config()

        self.pw_client = SecretsDataJSONClient(
            pw_config.creds_dir, pw_config.creds_file_name)
        self.crypto = SynchronousEncryptionFernet(pw_config.encryption_key)
        self.args: argparse.Namespace = None # set later with "setattr()"
    
    @staticmethod
    def main(args: List[str] = None, pw_config: PWConfig = None):

        if pw_config is None:
            pw_config = get_prod_config()
        
        if args is None:
            args = sys.argv[1:]
        
        if not isinstance(args, list):
            raise TypeError("Make sure to pass a list of strings. " \
                            f"You passed: {type(args)}")

        pw = PasswordCommand(pw_config)
        args = PasswordCommand.parse_args(args)
        setattr(pw, "args", args)

        # pw -d
        if args.debug:
            pprint(args.__dict__)
            print('')

        # pw -as
        if args.all_sections:
            pprint(pw.get_all_sections())
            return True

        # pw --all_secrets
        if args.list_keys:
            pw.print_all_keys(args.section)
            return True

        # pw -f <entity>
        args.find = args.entity # default --find
        if args.find:
            has_found = pw.find_secrets_data()
            if has_found is False:
                return False

        # pw -n <entity> (-kwargs)
        if args.new_secrets_data:
            return pw.add_new_secrets_data()

        # pw -u <key>=<value> <entity>
        if args.update:
            return pw.update_secrets_data()
        
        # pw -upw (<new_pw>) <entity> (-s <section>)
        # or: pw -f <entity> -upw (<new_pw>)
        # <new_pw> is optional, defaults to random pw
        # change random pw with -rl <int> and -rn
        if args.update_password:
            return pw.update_password()

        # pw -rm <entity>
        if args.remove_entity:
            return pw.remove_secrets_data()

        # pw -rms <section>
        if args.remove_section:
            return pw.remove_section()

        # pw -rn (no-special-characters)
        if args.no_special_characters is False:
            # "-rn" will activate "-r"
            args.generate_random_pw = True

        # pw -rl <length: int>
        if args.random_password_length != 42:
            # "-rl <int>" will activate "-r"
            args.generate_random_pw = True

        # pw -r
        if args.generate_random_pw:
            random_pw = pw.get_random_pw()
            pyperclip.copy(random_pw)
            print('The random password has been copied into your clipboard.')
            print('')
            return True

        # pw -s <section>
        if (
            args.section
            and not args.entity
        ):
            try:
                # Print keys of section if exists
                return pw.print_keys_of_section()
            except KeyError:
                # Create section if not exists
                return pw.create_section()

        if args.entity is None:
            print('Nothing happened. No flags used. No args passed after pw command.')
            return False

        secrets_data = pw.get_secrets_data()

        # pw -ks
        if args.available_keys:
            print(f'There are {len(secrets_data.keys())} available keys for {args.entity}:')
            print(', '.join(secrets_data.keys()))
            return True

        # pw -e <entity>
        args.expressive = True # default --expressive
        if args.expressive:
            pw.print_secrets_data_values(secrets_data)

        # pw <entity>
        if args.entity:
            pw = pw.get_secrets_data_value(secrets_data)
            pyperclip.copy(pw)
            print(f'Copied {args.secret_key} for "{args.entity}" into your clipboard.')
            print('')
            return
    
    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser(description='Manage your passwords from your terminal.')
        parser.add_argument('entity', type=str, help=h.entity, nargs='?')

        parser.add_argument('-d', '--debug', action='store_true')

        parser.add_argument('-f', '--find', type=str)
        parser.add_argument('-k', '--secret_key', type=str, default='password')
        parser.add_argument('-ks', '--available_keys', action='store_true')
        parser.add_argument('-e', '--expressive', action='store_true')
        parser.add_argument('-as', '--all_sections', action='store_true', help=h.all_sections)
        parser.add_argument('-ls', '--list-keys', action='store_true')
        parser.add_argument('-s', '--section', type=str, help=h.section)

        parser.add_argument('-r', '--generate_random_pw', action='store_true', help=h.generate_random_pw)
        parser.add_argument('-rl', '--random_password_length', type=int, default=42)
        parser.add_argument('-rn', '--no_special_characters', action='store_false')

        parser.add_argument('-n', '--new_secrets_data', type=str, help=h.add_new_password)
        parser.add_argument('-u', '--update', type=str)
        parser.add_argument('-upw', '--update_password', action='store_true')
        parser.add_argument('-pw', '--set_password', type=str, help=h.set_password)
        parser.add_argument('-un', '--username', type=str)
        parser.add_argument('-w', '--website', type=str)
        parser.add_argument('-kwargs', '--kwargs', '--keyword_arguments', type=str)
        parser.add_argument('-ow', '--overwrite', action='store_false')

        parser.add_argument('-rm', '--remove_entity', type=str, help=h.remove)
        parser.add_argument('-rms', '--remove_section', type=str, help=h.remove)

        return parser.parse_args(args)

    def get_all_sections(self) -> List[str]:
        """Get all sections of the secrets data file (json)."""
        return [pw for pw in self.pw_client.pw_dict.keys()]
        # yield from self.pw_dict.keys()

    def print_keys_of_section(self):
        """Output all available keys of a section to the console."""
        if self.args.section is None:
            self.args.section = 'main'
        for key in self.pw_client.pw_dict[self.args.section].keys():
            print(key)
    
    def print_all_keys(self, section: str = None):
        if section is None:
            for section, entities in self.pw_client.pw_dict.items():
                for entity in entities.keys():
                    print(f"({section}) {entity}")
        else:
            if self.pw_client.pw_dict.get(section) is None:
                print(f"Didn't find section \"{section}\"")
            for entity in self.pw_client.pw_dict[section].keys():
                print(entity)
            

    def create_section(self):
        """Creates a new section."""
        
        if self._check_existence_of_section(self.args.section):
            return print(f'Section {self.args.section} exists already.')

        self.pw_client.pw_dict[self.args.section] = {}
        self.pw_client.save_dict_to_file()
        print(f'Created a new section: "{self.args.section}".')
    
    def _check_existence_of_section(self, section: str):
        if section in self.pw_client.pw_dict:
            return True

    def add_new_secrets_data(self):
        secrets_data = {}

        if self.args.set_password:
            new_password = self.args.set_password
        else:
            new_password = generate_random_password(
                password_length=self.args.random_password_length,
                special_characters=self.args.no_special_characters)
        pyperclip.copy(new_password)
        encrypted_password = self.crypto.encrypt(new_password)
        secrets_data['password'] = encrypted_password

        if self.args.username:
            encrypted_username = self.crypto.encrypt(self.args.username)
            secrets_data['username'] = encrypted_username

        if self.args.website:
            encrypted_website = self.crypto.encrypt(self.args.website)
            secrets_data['website'] = encrypted_website

        if self.args.kwargs:
            kwargs_as_list = self.args.kwargs.split(',')
            for kwarg in kwargs_as_list:
                if len(kwarg.split('=')) > 2:
                    print('There is something wrong with your kwargs ...')
                    print('Expected format:')
                    print('"pw --kwargs brand=fender,guitar=strat,string_gauge=0.10"')
                    print('')
                key, value = kwarg.split('=')
                encrypted_value = self.crypto.encrypt(value)
                secrets_data[key] = encrypted_value

        if self.args.section is None:
            self.args.section = 'main'

        if not self._check_existence_of_section(self.args.section):
            self.create_section()

        if (
            self.args.entity in self.pw_client.pw_dict[self.args.section]
            and self.args.overwrite is False
        ):
            print('Entity is already there. Nothing happened.')
            print('Use the -ow / --overwrite option to update existing secrets data.')
            return False

        entity = self.args.new_secrets_data
        new_secrets_data = {entity: secrets_data}

        print(f'Created new password for "{entity}".')
        print('')

        self.pw_client.pw_dict[self.args.section].update(new_secrets_data)
        self.pw_client.save_dict_to_file()
        return True

    def update_secrets_data(self):
        """`pw -u <key>=<value> (-s <section>="main") <entity>`"""
        s = self.args.update
        split_at: int
        for i in range(len(s)):
            if s[i] == "=":
                split_at = i
                break
        
        k = s[:split_at]
        v = s[(split_at + 1):]
        
        new_data = {k: self.crypto.encrypt(v)}
        
        if self.args.section is None:
            self.args.section = 'main'
              
        self.pw_client.pw_dict[self.args.section][self.args.entity].update(new_data)
        self.pw_client.save_dict_to_file()
        print(f"Updated value of \"{k}\" of \"{self.args.entity}\"")
    
    def update_password(self):
        """Updates a password.
        
        Example usage:
        
        pw aws -upw
        (Generates a new random password for aws)
        
        pw aws -upw -pw new_password
        (change password of "aws" with "new_password")
        
        pw aws -upw -rl 10 -rn
        (change password of "aws" with a random pw with 10 chars and without special chars)
        """
        secrets_data = self.get_secrets_data()
        old_pw = self.get_secrets_data_value(secrets_data)
        print(f"old pw: {old_pw}")
        if self.args.set_password:
            new_pw = self.args.set_password
        else:
            new_pw = self.get_random_pw()

        self.args.update = f"old_password={old_pw}"
        self.update_secrets_data()

        self.args.update = f"password={new_pw}"
        self.update_secrets_data()

        pyperclip.copy(new_pw)
        print("Copied new pw to your clipboard.")

    def get_secrets_data(self):
        if self.args.section is None:
            self.args.section = 'main'
        secrets_data = self.pw_client.pw_dict[self.args.section][self.args.entity]
        return secrets_data

    def remove_secrets_data(self):
        key = self.args.remove_entity
        section = self.args.section or 'main'
        self.pw_client.pw_dict[section].pop(key)
        self.pw_client.save_dict_to_file()
        print(f'Deleted {key} from {section}')
        print('')
        return True

    def remove_section(self):
        section = self.args.remove_section
        self.pw_client.pw_dict.pop(section)
        self.pw_client.save_dict_to_file()
        print(f'Removed Section: "{section}"')
        return True

    def find_secrets_data(self):
        results_as_generator = find_key(self.args.find, self.pw_client.pw_dict)
        results = list(results_as_generator)
        for result in results:
            print(f'Found "{result["entity"]}" in section "{result["section"]}".')
        if len(results) >= 1:
            self.args.entity = results[0]['entity']
            self.args.section = results[0]['section']
            return True
        else:
            print(f'No results found for the given search term "{self.args.find}"')
            print('')
            return False

    def get_random_pw(self):
        if self.args.entity is not None:
            random_pw = generate_random_password(
                password_length=self.args.random_password_length,
                special_characters=self.args.no_special_characters)
        else:
            random_pw = generate_random_password(
                password_length=self.args.random_password_length,
                special_characters=self.args.no_special_characters)
        return random_pw

    def print_secrets_data_values(self, secrets_data):
        print(f'Here are the values for "{self.args.entity}":')
        for key, value in secrets_data.items():
            if key == 'password':
                value = 'sensitive'
            else:
                value = self.crypto.decrypt(value)
            print(f'    {key}: {value}')
        print('')
        return True

    def get_secrets_data_value(self, secrets_data):
        encrypted_secret_value = secrets_data[self.args.secret_key]
        decrypted_secret_value = self.crypto.decrypt(encrypted_secret_value)
        return decrypted_secret_value


if __name__ == "__main__":
    print("Please use PasswordCommand.main() outside of the module.")
