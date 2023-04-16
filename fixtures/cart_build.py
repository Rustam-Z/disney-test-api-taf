import pytest


@pytest.fixture()
def create_fake_cart_superuser(client, create_fake_metro):

    def _fixture(**kwargs):
        payload, response, model = create_fake_metro()
        return payload, response, model

    yield _fixture
