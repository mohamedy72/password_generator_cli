from features.vault import init_vault


def main():
    init_vault("data/vault.json", "abc123456")


if __name__ == "__main__":
    main()
