from src.crypto.asymmetric_encryption import (
    decrypt,
    encrypt,
    generate_private_rsa_2048_key,
)


def test_asymmetric_crypto():
    prik = generate_private_rsa_2048_key()
    pubk = prik.public_key()
    message = "Message in a Bottle"
    encrypted_message = encrypt(bytes(message.encode("UTF-8")), pubk)
    decrypted_message = decrypt(encrypted_message, prik)
    assert message == decrypted_message.decode("UTF-8")
