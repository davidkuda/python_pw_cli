#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
"""
Execute this command to get pw from json into clipboard.

`pw <name>` -> Get the password of <name> from the section main
`pw <name> <section>` -> Get the password of <name> from the section <section>
`pw sections` -> Print all available sections
`pw section <section>` -> Print all available keys of <section>
"""
import sys
import json
import string
import random
import datetime
import argparse
import pyperclip
from config.pw_config import creds_file_path


def get_pws_from_json_file(file_path):
    """Loads json data into python to retrieve passwords that are stored as key value pairs."""
    with open(file_path) as pws:
        return json.load(pws)


def print_sections(pw_file: dict):
    """Print all keys of a dictionary (depth -> 1)."""
    for key in pw_file.keys():
        print(key)


def print_keys_of_section(pw_file: dict, section_name):
    """Output all available keys of a section to the console."""
    for key in pw_file[section_name].keys():
        print(key)


def get_pw(pw_file: dict, pw_key: str, section: str = 'main'):
    """Access a dictionary's data (pws[section][pw_key]) and copy value to clipboard."""
    pw = pw_file[section][pw_key]['password']
    pyperclip.copy(pw)


def create_backup(pw_dict: dict):
    """Create a backup of the dictionary with the passwords."""
    now = datetime.datetime.now().isoformat()
    pretty_now = now.split('.')[0].replace(':', '.')
    with open(f'./backups/{pretty_now}', 'w') as pw_file_json:
        json.dump(pw_dict, pw_file_json)


def generate_random_password():
    """Generates a random password with 42 characters of any type (letters, digits, special characters)."""
    characters = string.printable
    random_password = ''.join(random.choice(characters) for i in range(42))
    return random_password


def add_new_pw(pw_dict: dict, service: str, file_path: str, password: str = None, user_name: str = None,
               website: str = None, section: 'str' = 'main') -> None:
    """Adds a new password to the password file."""

    create_backup(pw_dict)

    if password is None:
        password = generate_random_password()

    new_password = {service: {}}
    new_password[service]['password'] = password
    new_password[service]['user_name'] = user_name if user_name else 'not specified'
    new_password[service]['website'] = website if website else 'not specified'

    pw_dict.update(new_password)

    with open(file_path, 'w') as pw_file_json:
        json.dump(pw_dict, pw_file_json)


def my_exchandler(type, value, traceback):
    """Set 'sys.excepthook' to myexchandler to avoid traceback.
     Credits: https://stackoverflow.com/questions/38598740/raising-errors-without-traceback
    """
    print(value)


def validate_user_input(args, num=1, response_msg='Pass an arg after pw'):
    """Validate if user has passed the correct number of args with the command."""
    try:
        args[num]
    except IndexError:
        sys.excepthook = my_exchandler
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


def argparse_action():
    pws = get_pws_from_json_file(creds_file_path)
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    parser.add_argument('-a', '--availability', action='store_true')
    parser.add_argument('-s', '--section', type=str)
    args = parser.parse_args()

    if args.availability:
        return print_keys_of_section(pws, args.input)

    if args.section:
        return get_pw(pws, args.section, args.input)

    if args.input == 'sections':
        return print_sections(pws)

    return get_pw(pws, args.input)


def main():
    # Encrypt pw file
    pws = get_pws_from_json_file(creds_file_path)
    args = sys.argv
    validate_user_input(args)
    user_input = args[1:]

    if user_input[0] == 'sections':
        return print_sections(pws)

    if user_input[0] == 'section':
        validate_user_input(user_input, 1, 'add arg after section')
        section = user_input[1]
        return print_keys_of_section(pws, section)

    pw_key = user_input[0]

    if len(user_input) == 1:
        return get_pw(pws, pw_key)

    if len(user_input) > 1:
        pw_category = user_input[1]
        return get_pw(pws, pw_key, pw_category)

    # Decrypt pw file


if __name__ == '__main__':
    argparse_action()
