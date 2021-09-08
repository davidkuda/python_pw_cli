#!/opt/homebrew/Caskroom/miniconda/base/bin/python
import argparse
from pprint import pprint

import pyperclip

from pw_config import CREDS_DIR, CREDS_FILE_PATH, ENCRYPTION_KEY
from pw_client import PasswordClient
from pw_encryption import SynchronousEncryption
from utils import arg_help_texts as h


class PasswordCommand:
    def __init__(self, pw: PasswordClient,
                 crypto: SynchronousEncryption,
                 args: argparse.ArgumentParser):
        self.pw = pw
        self.crypto = crypto
        self.args = args

    def add_new_secrets_data(self):
        args = self.args

        secrets_data = {}

        if args.set_password:
            new_password = args.set_password
        else:
            new_password = self.pw.generate_random_password(
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

        self.pw.add_new_secrets_data(entity=args.new_secrets_data,
                                     secrets_data=secrets_data,
                                     section=args.section,
                                     overwrite=args.overwrite)

        return True

    def find_secrets_data(self):
        results_as_generator = self.pw.find_key(self.args.find)
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

    def generate_random_pw(self):
        if self.args.entity is not None:
            random_pw = self.pw.generate_random_password(
                password_length=self.args.random_password_length,
                special_characters=self.args.no_special_characters)
        else:
            random_pw = self.pw.generate_random_password(
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


# TODO: Can I attach a callable / function directly to arg parse so
# TODO: that I can avoid the long if / else statements below?
def parse_args():
    parser = argparse.ArgumentParser(description='Manage your passwords from your terminal.')
    parser.add_argument('entity', type=str, help=h.entity, nargs='?')

    parser.add_argument('-d', '--debug', action='store_true')

    parser.add_argument('-f', '--find', type=str)
    parser.add_argument('-k', '--secret_key', type=str, default='password')
    parser.add_argument('-ks', '--available_keys', action='store_true')
    parser.add_argument('-e', '--expressive', action='store_true')
    parser.add_argument('-as', '--all_sections', action='store_true', help=h.all_sections)
    parser.add_argument('-s', '--section', type=str, help=h.section)

    parser.add_argument('-r', '--generate_random_pw', action='store_true', help=h.generate_random_pw)
    parser.add_argument('-rl', '--random_password_length', type=int, default=42)
    parser.add_argument('-rn', '--no_special_characters', action='store_false')

    parser.add_argument('-n', '--new_secrets_data', type=str, help=h.add_new_password)
    parser.add_argument('-pw', '--set_password', type=str, help=h.set_password)
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-w', '--website', type=str)
    parser.add_argument('-kwargs', '--kwargs', '--keyword_arguments', type=str)
    parser.add_argument('-ow', '--overwrite', action='store_true')

    parser.add_argument('-rm', '--remove_entity', type=str, help=h.remove)
    parser.add_argument('-rms', '--remove_section', type=str, help=h.remove)

    args = parser.parse_args()
    return args


def main():
    # TODO: I am currently using two interfaces: pw and pw_client. Only use pw.
    args = parse_args()
    crypto = SynchronousEncryption(ENCRYPTION_KEY)
    pw_client = PasswordClient(CREDS_DIR, CREDS_FILE_PATH)
    pw = PasswordCommand(pw_client, crypto, args)

    if args.debug:
        pprint(args.__dict__)
        print('')

    if args.all_sections:
        return pw_client.print_sections()

    if args.find:
        has_found = pw.find_secrets_data()
        if has_found is False:
            return

    if args.new_secrets_data:
        return pw.add_new_secrets_data()

    if args.remove_entity:
        return pw_client.remove_entity(entity=args.remove_entity,
                                       section=args.section)

    if args.remove_section:
        return pw_client.remove_section(args.remove_section)

    # TODO: Move logic of "create new section if not exists" to client
    if args.section and not args.entity:
        try:
            return pw_client.print_keys_of_section(args.section)
        except KeyError:
            return pw_client.create_section(args.section)

    if args.no_special_characters is False:
        # "args.no_special_characters" stores False. Thus, if passed, it will be falsey.
        # A good user experience is to avoid passing "pw -r -rn" and just enable "pw -rn"
        # to generate a new random password without special characters.
        # Thus, "-rn" will activate "-r".
        args.generate_random_pw = True

    if args.random_password_length != 42:
        # Same as above with "args.no_special_characters": This control flow is designed to
        # improve the user experience. Instead of using "pw -r -rl 20" for a random pw with
        # a length of 20, we can instead just use "pw -rl 20".
        args.generate_random_pw = True

    # TODO: Move function "generate_random_pw" from pw_client to utils
    if args.generate_random_pw:
        pw.generate_random_pw()
        return True

    if args.entity is None:
        print('Nothing happened. No flags used. No args passed after pw command.')
        return False

    secrets_data = pw_client.get_secrets_data(entity=args.entity, section=args.section)

    if args.available_keys:
        print(f'There are {len(secrets_data.keys())} available keys for {args.entity}:')
        print(', '.join(secrets_data.keys()))
        return True

    if args.expressive:
        pw.print_secrets_data_values(secrets_data)

    if args.entity:
        return pw.get_secrets_data_value(secrets_data)


if __name__ == '__main__':
    main()
