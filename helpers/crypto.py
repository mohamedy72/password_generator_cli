import secrets
import base64
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
    """
    A function to derive a key from a master password, then use it to encrypt / decrypt data
    """
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

    return base64.urlsafe_b64encode(key)


def encrypt_data(data: str, key: bytes):
    """
    Function to encrypt the incoming data using a Derived key
    """
    cipher = Fernet(key)

    # This returns a token not raw encrypted bytes
    encrypted_msg = cipher.encrypt(data.encode())

    return encrypted_msg


def decrypt_data(token: bytes, key: bytes):
    """
    Function to decrypt data using a token
    """
    cipher = Fernet(key)

    decrypted_msg = cipher.decrypt(token)

    return decrypted_msg.decode()


def verify_master_password(token, key):
    cipher = Fernet(key)
    try:
        # comment:
        decrypted_msg = cipher.decrypt(token)
        if decrypted_msg == b"verified":
            return True
    except Exception as _:
        return False
    # end try
