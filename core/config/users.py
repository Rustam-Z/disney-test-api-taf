import random

from core.config import CONFIG
from core.enums.users import User


def get_random_user(user_type: User) -> tuple:
    users = CONFIG.users.get(user_type.value)

    user = random.choice(users)
    email, password = user.get('email'), user.get('password')

    return email, password
