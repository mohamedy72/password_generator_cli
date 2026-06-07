from pathlib import Path
from helpers import (
    generate_salt,
    derive_key,
    encrypt_data,
    save_vault,
    load_vault,
    verify_master_password,
    decrypt_data,
)


def init_vault(filename: str, password: str) -> None:
    pa = Path(filename).absolute()
    # 1. Validate path, create parent directories if needed
    if pa.suffix != ".json":
        raise ValueError("Only JSON files are supported")
    if not pa.exists():
        # Create parent directories if not exist
        pa.parent.mkdir(parents=True, exist_ok=True)

    # 2. Generate Salt
    salt = generate_salt()
    # 3. Derive key from master password + salt
    key = derive_key(password, salt)
    # 4. Create verification token — encrypt "verified" with key
    token = encrypt_data("verified", key).decode()
    # 5. Build initial vault structure — salt, empty entries
    vault_structure = {"salt": salt, "verification_token": token, "entries": {}}

    # 6. Serialize to JSON → save to disk
    save_vault(pa, vault_structure)


def unlock_vault(filename: str, password: str) -> dict:
    pa = Path(filename).absolute()

    if not pa.exists():
        raise FileNotFoundError(
            "Specified file don't exist. Either check spelling or run --init-vault "
        )
    # 1. Load JSON file → parse it
    data = load_vault(pa)

    # 2. Read salt from plain text field
    salt = data["salt"]

    # 3. Derive key from password + salt
    key = derive_key(password, salt)

    # 4. Decrypt verification token → verify password
    if verify_master_password(data["verification_token"].encode(), key):
        # TODO: Handle decryption if entries has data
        return data
    else:
        raise ValueError("Password verification failed")
