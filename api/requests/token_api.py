from api.http_client import HTTPClient
from api.responses.token_model import TokenSuccessResponse
from api.api_response import APIResponse


class TokenAPI:
    USER_TOKEN = '/user/token/'

    def __init__(self, client: HTTPClient):
        self.client = client

    def login(self, email: str, password: str) -> TokenSuccessResponse:
        payload = {
            'email': email,
            'password': password
        }
        response = self.client.post(self.USER_TOKEN, data=payload)
        APIResponse(response).check_status(200)

        model = TokenSuccessResponse(**response.json())
        return model
