from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse
from api.response_models.user.token_models import TokenSuccessResponse, RefreshTokenSuccessResponse


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
        response_payload = response.content

        if response.status_code == 200:
            response_payload = TokenSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def refresh_token(self, refresh: str, **kwargs) -> tuple:
        data = {
            'refresh': refresh,
        }
        response = self.client.post(self.USER_TOKEN_REFRESH, json=data, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = RefreshTokenSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
