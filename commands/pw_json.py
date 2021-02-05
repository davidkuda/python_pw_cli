#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
"""
Execute this command to get pw from json into clipboard.
"""
import sys
import os
import json
# import argparse
import pyperclip


file_path = ''


def get_pws_from_json_file(file_path):
    with open(file_path) as pws:
        return json.load(pws)


def print_sections(d):
    for key in d.keys():
        print(key)


def print_keys_of_section(d, section_name):
    for key in d[section_name].keys():
        print(key)


def get_pw(pws, pw_key, pw_category='uncategorized'):
    pw = pws[pw_category][pw_key]
    pyperclip.copy(pw)


def my_exchandler(type, value, traceback):
    """Set 'sys.excepthook' to myexchandler to avoid traceback.
     Credits: https://stackoverflow.com/questions/38598740/raising-errors-without-traceback
    """
    print(value)


def validate_user_input(args, num=1, response_msg='Pass an arg after pw'):
    try:
        args[num]
    except IndexError:
        sys.excepthook = my_exchandler
        raise IndexError(response_msg)
    else:
        pass


def main():
    pws = get_pws_from_json_file(file_path)
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


if __name__ == '__main__':
    main()