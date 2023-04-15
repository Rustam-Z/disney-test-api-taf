from core.http_client import HTTPClient
from api.responses.response_models import ErrorResponse
from api.responses.user.token_model import (TokenSuccessResponse,
                                            RefreshTokenSuccessResponse,
                                            )


class TokenAPI:
    USER_TOKEN = '/user/token/'
    USER_TOKEN_REFRESH = '/user/token/refresh/'

    def __init__(self, client: HTTPClient):
        self.client = client

    def login(self, email: str, password: str, **kwargs) -> tuple:
        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(self.USER_TOKEN, json=data, **kwargs)

        if response.status_code in range(200, 300):
            model = TokenSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def refresh_token(self, refresh: str, **kwargs) -> tuple:
        data = {
            'refresh': refresh,
        }
        response = self.client.post(self.USER_TOKEN_REFRESH, json=data, **kwargs)

        if response.status_code in range(200, 300):
            model = RefreshTokenSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model
