import argparse
from pprint import pprint
from typing import List

import pyperclip

from .pw_json_client import SecretsDataJSONClient
from .pw_utils import generate_random_password
from crypto.pw_encryption import SynchronousEncryption


class PasswordCommand:
    def __init__(self, pw_client: SecretsDataJSONClient,
                 crypto: SynchronousEncryption,
                 args: argparse.ArgumentParser):
        self.pw_client = pw_client
        self.crypto = crypto
        self.args = args

    def get_all_sections(self) -> List[str]:
        return self.pw_client.get_sections()

    def print_keys_of_section(self):
        if self.args.section is None:
            self.args.section = 'main'
        self.pw_client.print_keys_of_section(self.args.section)

    def create_section(self):
        return self.pw_client.create_section(self.args.section)

    def add_new_secrets_data(self):
        args = self.args

        secrets_data = {}

        if args.set_password:
            new_password = args.set_password
        else:
            new_password = generate_random_password(
                password_length=args.random_password_length,
                special_characters=args.no_special_characters)
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

        self.pw_client.add_new_secrets_data(entity=args.new_secrets_data,
                                     secrets_data=secrets_data,
                                     section=args.section,
                                     overwrite=args.overwrite)

        return True

    def update_secrets_data(self):
        """`pw -u <key>=<value> <entity>`"""
        k, v = self.args.update.split('=')
        new_data = {k: self.crypto.encrypt(v)}
        self.pw_client.update_secrets_data(
            entity=self.args.entity,
            section=self.args.section,
            new_data=new_data)

    def get_secrets_data(self):
        secrets_data = self.pw_client.get_secrets_data(
            entity=self.args.entity,
            section=self.args.section)
        return secrets_data

    def remove_secrets_data(self):
        key = self.args.remove_entity
        self.pw_client.remove_secrets_data(key, self.args.section)
        return True

    def remove_section(self):
        self.pw_client.remove_section(self.args.remove_section)
        return True

    def find_secrets_data(self):
        results_as_generator = self.pw_client.find_key(self.args.find)
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
        pyperclip.copy(random_pw)
        print('The random password has been copied into your clipboard.')
        print('')
        return True

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
        pyperclip.copy(decrypted_secret_value)
        print(f'Copied {self.args.secret_key} for "{self.args.entity}" into your clipboard.')
        print('')
        return True
