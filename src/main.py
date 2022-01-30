#!/opt/homebrew/Caskroom/miniconda/base/bin/python
import argparse
from pprint import pprint

from pw.pw_cli import PasswordCommand
from pw.pw_config import CREDS_DIR, CREDS_FILE_PATH, ENCRYPTION_KEY
from pw.pw_json_client import SecretsDataJSONClient
from crypto.synchronous_encryption_fernet import SynchronousEncryptionFernet
from pw.pw_utils import HelpTexts as h


def main():
    args = parse_args(sys.argv[1:])
    crypto = SynchronousEncryptionFernet(ENCRYPTION_KEY)
    pw_json_client = SecretsDataJSONClient(CREDS_DIR, CREDS_FILE_PATH)
    pw = PasswordCommand(pw_json_client, crypto, args)

    # pw -d
    if args.debug:
        pprint(args.__dict__)
        print('')

    # pw -as
    if args.all_sections:
        pprint(pw.get_all_sections())
        return True

    # pw -f <entity>
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
        pw.get_random_pw()
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
    if args.expressive:
        pw.print_secrets_data_values(secrets_data)

    # pw <entity>
    if args.entity:
        return pw.get_secrets_data_value(secrets_data)

# TODO: Can I attach a callable / function directly to arg parse?
# -> How to avoid the complex if / else control flow in "main()"?
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
    parser.add_argument('-u', '--update', type=str)
    parser.add_argument('-pw', '--set_password', type=str, help=h.set_password)
    parser.add_argument('-un', '--username', type=str)
    parser.add_argument('-w', '--website', type=str)
    parser.add_argument('-kwargs', '--kwargs', '--keyword_arguments', type=str)
    parser.add_argument('-ow', '--overwrite', action='store_false')

    parser.add_argument('-rm', '--remove_entity', type=str, help=h.remove)
    parser.add_argument('-rms', '--remove_section', type=str, help=h.remove)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
