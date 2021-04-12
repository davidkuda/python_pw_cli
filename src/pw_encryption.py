from cryptography.fernet import Fernet


class SynchronousEncryption:
    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)

    def encrypt(self, text: str):
        encrypted_text = self.cipher.encrypt(text.encode('utf-8'))
        return encrypted_text

    def decrypt(self, encrypted_text: bytes):
        """Decrypt an encrypted text."""
        decrypted_text = self.cipher.decrypt(encrypted_text)
        return decrypted_text.decode()

    @staticmethod
    def generate_key():
        """Generate Key for synchronous encryption.

        Save the string that this function returns to the file "pw_config.py" as
        the constant "ENCRYPTION_KEY". Pass it to init of this class."""
        return Fernet.generate_key()


def encrypt_async():
    pass


if __name__ == '__main__':
    print(SynchronousEncryption.generate_key())
