import pytest

from core.config import CONFIG
from core.enums.environments import Environment
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
