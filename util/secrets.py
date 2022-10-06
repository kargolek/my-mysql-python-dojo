import os


class Secrets:
    KEY = os.environ.get("decrypt_key")
