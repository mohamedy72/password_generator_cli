import secrets
import string


def generate_password(length: int) -> str:
    combination = string.ascii_letters + string.digits + "_-*#$^"
    password = "".join(secrets.choice(combination) for i in range(length))

    return password
