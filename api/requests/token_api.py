from api.http_client import HTTPClient
from api.responses.token_model import TokenSuccessResponse, TokenErrorResponse


class TokenAPI:
    USER_TOKEN = '/user/token/'

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
            model = TokenErrorResponse(**response.json())

        return response, model
