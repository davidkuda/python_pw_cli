#!/opt/homebrew/Caskroom/miniconda/base/bin/python
import argparse

import pyperclip

from pw_config import CREDS_DIR, CREDS_FILE_PATH, ENCRYPTION_KEY
import pw_client
from pw_encryption import SynchronousEncryption

HELP_TEXT = {
    'entity': 'Name of entity that holds the password.',
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


# TODO: Can I attach a callable / function directly to arg parse so
# TODO: that I can avoid the exhaustingly long if / else statements below?
def parse_args():
    parser = argparse.ArgumentParser(description='Manage your passwords from your terminal.')
    parser.add_argument('entity', type=str, help=HELP_TEXT['entity'], nargs='?')

    parser.add_argument('-k', '--secret_key', type=str, default='password')
    parser.add_argument('-ks', '--available_keys', action='store_true')
    parser.add_argument('-f', '--full', action='store_true')
    parser.add_argument('-as', '--all_sections', action='store_true', help=HELP_TEXT['all_sections'])
    parser.add_argument('-s', '--section', type=str, help=HELP_TEXT['section'])
    parser.add_argument('-r', '--generate_random_pw', action='store_true', help=HELP_TEXT['generate_random_pw'])
    parser.add_argument('-rl', '--random_password_length', type=int, default=42)

    parser.add_argument('-n', '--new_secrets_data', type=str, help=HELP_TEXT['add_new_password'])
    parser.add_argument('-pw', '--set_password', type=str, help=HELP_TEXT['set_password'])
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-w', '--website', type=str)
    parser.add_argument('--kwargs', '--keyword_arguments', type=str)
    parser.add_argument('-ow', '--overwrite', action='store_true')

    parser.add_argument('-rm', '--remove_entity', type=str, help=HELP_TEXT['remove'])
    parser.add_argument('-rms', '--remove_section', type=str, help=HELP_TEXT['remove'])

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    crypto = SynchronousEncryption(ENCRYPTION_KEY)
    pw = pw_client.PasswordClient(CREDS_DIR, CREDS_FILE_PATH)

    if args.all_sections:
        return pw.print_sections()

    if args.new_secrets_data:
        secrets_data = {}

        if args.set_password:
            new_password = args.set_password
        else:
            new_password = pw.generate_random_password(password_length=args.random_password_length)
        encrypted_password = crypto.encrypt(new_password)
        secrets_data['password'] = encrypted_password

        if args.username:
            encrypted_username = crypto.encrypt(args.username)
            secrets_data['username'] = encrypted_username

        if args.website:
            encrypted_website = crypto.encrypt(args.website)
            secrets_data['website'] = encrypted_website

        if args.kwargs:
            kwargs_as_list = args.kwargs.split(',')
            for kwarg in kwargs_as_list:
                if len(kwarg.split('=')) > 2:
                    print('There is something wrong with your kwargs ...')
                    print('Desired format:')
                    print('"pw --kwargs brand=fender,guitar=strat,string_gauge=0.10"')
                    print('')
                key, value = kwarg.split('=')
                encrypted_value = crypto.encrypt(value)
                secrets_data[key] = encrypted_value

        pw.add_new_secrets_data(entity=args.new_secrets_data,
                                secrets_data=secrets_data,
                                section=args.section,
                                overwrite=args.overwrite)

        return True

    if args.remove_entity:
        return pw.remove_entity(entity=args.remove_entity, section=args.section)

    if args.remove_section:
        return pw.remove_section(args.remove_section)

    # TODO: Move logic of "create new section if not exists" to client
    if args.section and not args.entity:
        try:
            return pw.print_keys_of_section(args.section)
        except KeyError:
            return pw.create_section(args.section)

    # TODO: Move function "generate_random_pw" from pw_client to utils
    if args.generate_random_pw:
        if args.entity is not None:
            random_pw = pw.generate_random_password(password_length=args.random_password_length)
        else:
            random_pw = pw.generate_random_password(password_length=args.random_password_length)
        pyperclip.copy(random_pw)
        print('The random password has been copied into your clipboard.')
        print('')
        return random_pw

    if args.entity is None:
        print('Nothing happened. No flags used. No args passed after pw command.')
        return False

    secrets_data = pw.get_secrets_data(entity=args.entity, section=args.section)

    if args.available_keys:
        print(f'There are {len(secrets_data.keys())} available keys for {args.entity}:')
        print(', '.join(secrets_data.keys()))
        return True

    if args.full:
        print('Here are the values:')
        for key, value in secrets_data.items():
            if key == 'password':
                value = 'sensitive'
            else:
                value = crypto.decrypt(value)
            print(f'    {key}: {value}')
        return True

    if args.entity:
        encrypted_secret_value = secrets_data[args.secret_key]
        decrypted_secret_value = crypto.decrypt(encrypted_secret_value)
        pyperclip.copy(decrypted_secret_value)
        print(f'Copied {args.secret_key} for "{args.entity}" into your clipboard.')
        print('')
        return True


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
