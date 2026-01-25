import hashlib


def encode_refresh_token(refresh_token: str):
    token_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()

    return token_hash