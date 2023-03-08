import time

import jwt


def decode_jwt(token: str) -> dict:
    """
    Function that reads data encoded into JWT.
    """
    data = jwt.decode(token, options={'verify_signature': False})
    return data


def is_jwt_expired(token: str, offset: int = 30) -> bool:
    """
    Function that validates that JWT token is not expired.
    """
    key = 'exp'
    token_expiration_time = decode_jwt(token)[key]
    current_time = int(time.time())
    expiration_time = (token_expiration_time - current_time - offset)
    return expiration_time < 0
