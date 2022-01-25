import json
import random
import string
from typing import Generator


class HelpTexts:
    entity = 'Name of entity that holds the password.',
    all_sections = 'Print all available sections.',
    section = '''
    Pass a section to print all entities of that section.
    The -s flag can be used together with other functions:
    Use it with "-add_new_password" to write pw to a specific section:
    "pw -n GitHub -s dev" -- Writes a new random password for "GitHub" to the section "dev";
    Use it with an argument without a flag to get a password from a specific section:
    "pw -s dev GitHub" -- Gets password for "GitHub" from the section "dev"''',
    add_new_password = 'Pass an entity as arg and add a new password to the json file.',
    generate_random_pw = 'Print a randomly generated password and add it to your clipboard.',
    remove = '''
    Delete a password from the creds file. Combine together with "-s" 
    if the password you want to delete is in an other section than "main".
    Example: "pw -d GitHub -s dev" -> Remove the password for GitHub
    from the section "dev".''',
    set_password = 'Set your own password instead of generating a random password. Use it with "-n".'


def generate_random_password(special_characters=True, 
                             password_length: int = 42) -> str:
        """Generates a random password and returns it as a string."""
        digits = string.digits
        letters = string.ascii_letters
        punctuation = r"!#$%&()*+:,-./;<=>?@[]^_{|}~" if special_characters else ''
        characters = digits + letters + punctuation
        random_password = ''.join(random.choice(characters) for i in range(password_length))
        return random_password
    

def my_exchandler(type, value, traceback):
    """Set 'sys.excepthook' to myexchandler to avoid traceback.
     Credits: https://stackoverflow.com/questions/38598740/raising-errors-without-traceback
    """
    print(value)


def find_key(key: str, dictionary: dict) -> Generator[dict, None, None]:
    """Iterate a dict recursively and yield all values if key matches."""
    for section, secrets in dictionary:
        for secret in secrets:
            if key.lower() in secret.lower():
                yield {'entity': secret, 'section': section}
