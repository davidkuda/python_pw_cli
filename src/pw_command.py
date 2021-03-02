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


def main():
    pw = pw_client.PasswordClient(CREDS_DIR, CREDS_FILE_PATH)
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    parser.add_argument('-a', '--availability', action='store_true')
    parser.add_argument('-s', '--section', type=str)
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
