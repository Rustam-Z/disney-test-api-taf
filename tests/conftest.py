import pytest

from api.requests.token_api import TokenAPI
from core.config import CONFIG
from data.users import get_config_user
from core.enums.environments import Environment
from core.enums.users import User
from core.helpers.jwt_helper import is_jwt_expired
from core.http_client import HTTPClient


CACHED_ACCESS_TOKENS = {}  # email: access_token


@pytest.hookimpl
def pytest_addoption(parser):
    choices = [member.value for member in Environment]
    parser.addoption('--env', action='store', choices=choices, default=CONFIG.env)


@pytest.hookimpl
def pytest_configure(config):
    """PyTest's configuration hook.

    The default "env" is specified in ".config.yaml". If "--env" is not specified "env" in ".config.yaml" will be used.
    If "--env" is specified, then the "CONFIG.env" will be overridden, and tests ONLY will run on specified environment.
    But if you try to run individual modules, they will run on environment specified in "env" in ".config.yaml".
    """
    env = config.getoption('--env')
    CONFIG.env = env
    CONFIG.hosts = CONFIG[env].hosts
    CONFIG.users = CONFIG[env].users


@pytest.fixture(scope='session', autouse=True)
def client(request):
    api_url = CONFIG.hosts.api + CONFIG.prefix
    request.session.client = HTTPClient(api_url)
    yield request.session.client
    request.session.client.session.close()


@pytest.fixture(autouse=True)
def users(request):
    """
    Authorizes user request.

    Steps:
        - Select user depending on `user` param value from core.enums.users.User.
        - Get user credentials (email, password) using get_config_user()
        - Request user token. And cache user token. Use cached value next time.
    """
    client = request.session.client
    user_type = request.node.callspec.params.get('user')  # Don't change `user`. You should change @users, and `user`
    # param in tests if you change user here.

    if user_type is User.NONE:
        # Remove Authorization header
        client.remove_headers('Authorization')
    else:
        # Update headers with Authorization header
        email, password = get_config_user(user_type)
        access_token = get_access_token(client, email, password)
        headers = {
            'Authorization': 'Bearer ' + access_token,
        }
        client.update_headers(headers)


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
