import pytest

from api.requests.token_api import TokenAPI
from core.config import CONFIG
from core.config.users import get_random_user
from core.enums.environments import Environment
from core.enums.users import User
from core.http_client import HTTPClient


@pytest.hookimpl
def pytest_addoption(parser):
    choices = [member.value for member in Environment]
    parser.addoption('--env', action='store', choices=choices, default=CONFIG.env)


@pytest.hookimpl
def pytest_configure(config):
    """PyTest configuration hook.

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
        - Get user credentials (email, password) using config.users.get_random_user()
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
        email, password = get_random_user(user_type)
        response, model = TokenAPI(client).login(email=email, password=password)
        access_token = model.data.access
        headers = {
            'Authorization': 'Bearer ' + access_token,
        }
        client.update_headers(headers)
