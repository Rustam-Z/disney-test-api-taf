from core.http_client import HTTPClient
from api.responses.response_models import ErrorResponse
from api.responses.token_model import (TokenSuccessResponse,
                                       RefreshTokenSuccessResponse,
                                       )


class TokenAPI:
    USER_TOKEN = '/user/token/'
    USER_TOKEN_REFRESH = '/user/token/refresh/'

    def __init__(self, client: HTTPClient):
        self.client = client

    def login(self, email: str, password: str) -> tuple:
        payload = {
            'email': email,
            'password': password
        }
        response = self.client.post(self.USER_TOKEN, data=payload)

        if response.status_code == 200:
            model = TokenSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def refresh_token(self, refresh: str) -> tuple:
        payload = {
            'refresh': refresh,
        }
        response = self.client.post(self.USER_TOKEN_REFRESH, data=payload)

        if response.status_code == 200:
            model = RefreshTokenSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model
