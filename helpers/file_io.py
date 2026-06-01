"""
This file is responsible on managing File I/O operations for the vault (Saving and Loading)
"""

from pathlib import Path
import json


def load_vault(path: str) -> bytes:
    """
    A function that returns bytes data from a provided path

    PARAMS:
        - path: string representaion of file path

    RETURNS:
        - bytes data
    """
    pa = Path(path).absolute()

    if not pa.exists():
        raise FileNotFoundError("File not found. Check file name or run --init-vault")

    with open(pa, "r") as f:
        data = json.load(f)

    return data


def save_vault(path: str, data: bytes) -> None:
    pa = Path(path).absolute()

    with open(pa, "wb") as f:
        f.write(data)
