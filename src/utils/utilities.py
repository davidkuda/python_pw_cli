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
