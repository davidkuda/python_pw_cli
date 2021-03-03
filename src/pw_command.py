#!/usr/local/bin/python3
"""
Execute this command to get pw from json into clipboard.

`pw <name>` -> Get the password of <name> from the section main
`pw sections` -> Print all available sections
`pw -a <section>` -> Print all available keys of <section>
`pw -s <section> <name>` -> Get the password of <name> from the section <section>

The creds.json file should look like this:

"section": {
        "service": {
            "password": "lorem",
            "user_name": "ipsum",
            "additional_info": "...",
            "website": "www.kuda.ai"
        }
    }
"""
import argparse
from pw_config import CREDS_DIR, CREDS_FILE_PATH
import pw_client
HELP_TEXT = {
        'get_password': 'Get a password. Pass entity as argument.',
        'all_sections': 'Print all available sections.',
        'section': 'Pass a section to print all entities of that section.',
        'generate_random_pw': 'Print a randomly generated password and add it to your clipboard.'
    }


def main():
    pw = pw_client.PasswordClient(CREDS_DIR, CREDS_FILE_PATH)
    parser = argparse.ArgumentParser(description='Manage your passwords from the terminal.')
    parser.add_argument('-g', '--get_password', type=str, help=HELP_TEXT['get_password'])
    parser.add_argument('-as', '--all_sections', action='store_true', help=HELP_TEXT['all_sections'])
    parser.add_argument('-s', '--section', type=str, help=HELP_TEXT['section'])
    parser.add_argument('-r', '--generate_random_pw', action='store_true', help=HELP_TEXT['generate_random_pw'])
    args = parser.parse_args()

    if args.availability:
        return pw.print_keys_of_section(args.input)

    if args.section:
        return pw.get_pw(args.section, args.input)

    if args.input == 'sections':
        return pw.print_sections()

    return pw.get_pw(args.input)


if __name__ == '__main__':
    main()
