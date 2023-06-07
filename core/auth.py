from api.endpoints.user.token_api import TokenAPI
from core.helpers.jwt_helper import is_jwt_expired
from core.http_client import HTTPClient

CACHED_ACCESS_TOKENS = {}  # email: access_token


def get_access_token(client: HTTPClient, email: str, password: str) -> str:
    access_token = CACHED_ACCESS_TOKENS.get(email)  # Check cache
    is_cached_access_token_expired = True

    if access_token is not None:
        is_cached_access_token_expired = is_jwt_expired(access_token)

    if access_token is None or is_cached_access_token_expired:
        response, model = TokenAPI(client).login(email=email, password=password)
        access_token = model.data.access
        CACHED_ACCESS_TOKENS[email] = access_token

    return access_token
