from typing import Any

import jwt
from datetime import datetime, timedelta
from faker import Faker


class CustomFaker(Faker):
    def __init__(self, **config: Any):
        super().__init__(**config)

    def jwt_token(self) -> str:
        exp_time = datetime.utcnow() + timedelta(hours=1)

        payload = {
            'sub': self.uuid4(),
            'name': self.name(),
            'email': self.email(),
            'iat': datetime.utcnow(),
            'exp': exp_time
        }
        token = jwt.encode(payload, self.text(), algorithm='HS256')

        return token
