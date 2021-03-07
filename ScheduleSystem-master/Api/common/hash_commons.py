import hashlib


def hash_md5(value: str) -> str:
    return hashlib.md5(bytes(value, encoding='utf8')).hexdigest()
