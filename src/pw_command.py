#!/opt/homebrew/Caskroom/miniconda/base/bin/python
"""
Execute this command to get pw from json into clipboard.
Type "pw -h" to get help on all available commands.
Basic usage: "pw <entity>" -> Gets password of entity from main section.

The creds.json file should look like this:

"section": {
        "entity": {
            "password": "lorem",
            "username": "ipsum",
            "additional_info": "...",
            "website": "www.kuda.ai"
        }
    }
"""
import argparse

import pyperclip

from pw_config import CREDS_DIR, CREDS_FILE_PATH
import pw_client
from pw_encryption import SynchronousEncryption
from pw_config import ENCRYPTION_KEY

HELP_TEXT = {
    'input': 'Name of entity that holds the password.',
    'all_sections': 'Print all available sections.',
    'section':
        '''Pass a section to print all entities of that section.
        The -s flag can be used together with other functions:
          Use it with "-add_new_password" to write pw to a specific section:
            "pw -n GitHub -s dev" -- Writes a new random password for "GitHub" to the section "dev";
          Use it with an argument without a flag to get a password from a specific section:
            "pw -s dev GitHub" -- Gets password for "GitHub" from the section "dev"''',
    'add_new_password': 'Pass an entity as arg and add a new password to the json file.',
    'generate_random_pw': 'Print a randomly generated password and add it to your clipboard.',
    'remove':
        '''Delete a password from the creds file. Combine together with "-s" 
        if the password you want to delete is in an other section than "main".
        Example: "pw -d GitHub -s dev" -> Remove the password for GitHub
        from the section "dev".''',
    'set_password': 'Set your own password instead of generating a random password. Use it with "-n".'
}


def parse_args():
    parser = argparse.ArgumentParser(description='Manage your passwords from your terminal.')
    parser.add_argument('input', type=str, help=HELP_TEXT['input'], nargs='?')
    parser.add_argument('-as', '--all_sections', action='store_true', help=HELP_TEXT['all_sections'])
    parser.add_argument('-s', '--section', type=str, help=HELP_TEXT['section'])
    parser.add_argument('-r', '--generate_random_pw', action='store_true', help=HELP_TEXT['generate_random_pw'])
    parser.add_argument('-n', '--add_new_password', type=str, help=HELP_TEXT['add_new_password'])
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-w', '--website', type=str)
    parser.add_argument('-pw', '--set_password', type=str, help=HELP_TEXT['set_password'])
    parser.add_argument('-rm', '--remove_password', type=str, help=HELP_TEXT['remove'])
    parser.add_argument('-rms', '--remove_section', type=str, help=HELP_TEXT['remove'])

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    crypto = SynchronousEncryption(ENCRYPTION_KEY)
    pw = pw_client.PasswordClient(CREDS_DIR, CREDS_FILE_PATH)

    # TODO: Get data inside pw_command.py
    # pw_data = pw.get_pw(???)

    if args.all_sections:
        return pw.print_sections()

    if args.add_new_password:
        if args.set_password:
            encrypted_password = crypto.encrypt(args.set_password)
        else:
            new_random_password = pw.generate_random_password()
            encrypted_password = crypto.encrypt(new_random_password)
        return pw.add_new_pw(entity=args.add_new_password, username=args.username,
                             website=args.website, section=args.section,
                             password=encrypted_password)

    if args.username:
        decrypted_username = pw.get_pw(args.username, 'username', args.section)
        encrypted_username = crypto.encrypt(decrypted_username)
        return encrypted_username

    if args.website:
        return pw.get_pw(args.website, 'website', args.section)

    if args.remove_password:
        return pw.remove_password(entity=args.remove_password, section=args.section)

    if args.remove_section:
        return pw.remove_section(args.remove_section)

    if args.section and args.input:
        encrypted_password = pw.get_pw(entity=args.input, section=args.section)
        password = crypto.decrypt(encrypted_password)
        return password

    if args.section:
        try:
            return pw.print_keys_of_section(args.section)
        except KeyError:
            return pw.create_section(args.section)

    if args.generate_random_pw:
        if args.input is not None:
            random_pw = pw.generate_random_password(password_length=int(args.input))
        else:
            random_pw = pw.generate_random_password()
        pyperclip.copy(random_pw)
        print('The random password has been copied into your clipboard.')
        print('')
        return random_pw

    if args.input is None:
        return print('Nothing happened. No flags used. No args passed after pw command.')

    if args.input:
        encrypted_password = pw.get_pw(args.input)
        decrypted_password = crypto.decrypt(encrypted_password)
        pyperclip.copy(decrypted_password)
        print(f'Copied {attribute} for "{entity}" into your clipboard.')
        print('')
        return encrypted_password


def decrypt_pw_file():
    pw = pw_client.PasswordClient(CREDS_DIR, CREDS_FILE_PATH)
    return pw.decrypt_all_passwords()


def encrypt_pw_file():
    pw = pw_client.PasswordClient(CREDS_DIR, CREDS_FILE_PATH)
    return pw.encrypt_all_passwords()


if __name__ == '__main__':
    main()

    # decrypt_pw_file()
    # encrypt_pw_file()

