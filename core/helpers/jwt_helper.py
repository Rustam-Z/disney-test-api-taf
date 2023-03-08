import jwt


def decode_jwt(token: str) -> dict:
    """
    Function that reads data encoded into JWT.

    Args:
        token: Any JWT (JSON Web Token).

    Returns: data that is encoded into token.

    """
    data = jwt.decode(token, options={'verify_signature': False})
    return data
