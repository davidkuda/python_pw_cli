import json
import random
import string


def generate_random_password(special_characters=True, 
                             password_length: int = 42) -> str:
        """Generates a random password and returns it as a string."""
        digits = string.digits
        letters = string.ascii_letters
        punctuation = r"!#$%&()*+:,-./;<=>?@[]^_{|}~" if special_characters else ''
        characters = digits + letters + punctuation
        random_password = ''.join(random.choice(characters) for i in range(password_length))
        return random_password


def get_pws_from_json_file(file_path):
    """Loads json data into python to retrieve passwords that are stored as key value pairs."""
    with open(file_path) as pws:
        return json.load(pws)


def my_exchandler(type, value, traceback):
    """Set 'sys.excepthook' to myexchandler to avoid traceback.
     Credits: https://stackoverflow.com/questions/38598740/raising-errors-without-traceback
    """
    print(value)
