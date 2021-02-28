#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
"""
Execute this command to get pw from json into clipboard.

`pw <name>` -> Get the password of <name> from the section main
`pw <name> <section>` -> Get the password of <name> from the section <section>
`pw sections` -> Print all available sections
`pw section <section>` -> Print all available keys of <section>
"""
import sys
import argparse
from commands.pw_config import creds_file_path
import pw_client


def argparse_action():
    pw = pw_client.PasswordClient(creds_file_path)
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
