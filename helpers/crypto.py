import secrets
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.fernet import Fernet


def generate_salt():
    """
    Genrate a salt of 32 hex characters to be used in password hashing

    RETURN:
        salt_string: hex encoded
    """
    randome_bytes = secrets.token_bytes(16)
    salt_string = randome_bytes.hex()

    return salt_string


def derive_key(password: str, salt: str) -> bytes:
    kdf = Argon2id(
        salt=bytes.fromhex(salt),
        length=32,
        iterations=1,
        lanes=4,
        memory_cost=64 * 1024,
        ad=None,
        secret=None,
    )
    # .encode() transfer str => Bytes
    key = kdf.derive(password.encode())

    return key


def encrypt_data(data: str, key: bytes):
    """
    Function to encrypt the incoming data using a Derived key
    """
    cipher = Fernet(key)

    encrypted_msg = cipher.encrypt(data.encode())

    return encrypted_msg


def decrypt_data(token: bytes, key: bytes):
    """
    Function to decrypt data using a token
    """
    cipher = Fernet(key)

    decrypted_msg = cipher.decrypt(token)

    return decrypted_msg.decode()
