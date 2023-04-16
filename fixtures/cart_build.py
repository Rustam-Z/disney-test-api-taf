import pytest

import data
from api.endpoints.metro.cart_build_api import CartBuildAPI


@pytest.fixture()
def create_fake_cart_superuser(client, create_fake_metro_superuser, create_fake_metro_item_configuration_superuser):
    def _fixture(**kwargs):
        # Arrange
        metro_payload, metro_response, metro_model = create_fake_metro_superuser()
        conf_payload, conf_response, conf_model = create_fake_metro_item_configuration_superuser()
        metro_qr_code = metro_model.data.qr_code
        metro_config_qr_code = conf_model.data.qr_code

        # Create cart
        payload = data.fake.model.cart(metro_qr_code=metro_qr_code, metro_config_qr_code=metro_config_qr_code, **kwargs)
        response, model = CartBuildAPI(client).create_cart(data=payload)

        return payload, response, model

    yield _fixture
