"""
This file is responsible on managing File I/O operations for the vault (Saving and Loading)
"""

import json


def load_vault(path: str) -> dict:
    with open(path, "r") as f:
        data = json.load(f)

    return data


def save_vault(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
