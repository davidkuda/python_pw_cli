#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
"""
Command gets pw into clipboard.
"""
import configparser
import sys
import os
# import argparse
import pyperclip


path = ''
config = configparser.ConfigParser()
config.read(path, encoding='UTF-8')


def get_keys():
    keys = config['pws'].keys()
    for key in keys:
        print(key)


def copy_pw():
    try:
        sys.argv[1]
    except IndexError:
        print('Pass an arg after pw')
    except Exception:
        raise
    else:
        user_input = sys.argv[1]
        pw = config['pws'][user_input]
        pyperclip.copy(pw)


if __name__ == '__main__':
    copy_pw()
