import random

from core.config import CONFIG
from core.enums.auth import Auth


def get_random_user(user_type: Auth) -> tuple:
    users = CONFIG.users.get(user_type.value)

    user = random.choice(users)
    email, password = user.get('email'), user.get('password')

    return email, password
