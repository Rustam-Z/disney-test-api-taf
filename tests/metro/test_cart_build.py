from api.endpoints.metro.cart_build_api import CartBuildAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
import data


class TestCreateCart:
    @users(User.SUPERUSER)
    def test_createCart_withValidData_returns200AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_cart_superuser')()

        # Assert
        APIResponse(response).assert_status(200)

    @users(User.SUPERUSER)
    def test_createCart_withMetroAndMetroConfigBelongingToDifferentFacility_returns200AndData(self, client, user, request):
        # Arrange
        metro_payload, metro_response, metro_model = request.getfixturevalue('create_fake_metro_superuser')()
        conf_payload, conf_response, conf_model = request.getfixturevalue('create_fake_metro_item_configuration_superuser')()
        metro_qr_code = metro_model.data.qr_code
        metro_config_qr_code = conf_model.data.qr_code

        # Act
        payload = data.fake.model.cart(metro_qr_code=metro_qr_code, metro_config_qr_code=metro_config_qr_code)
        response, model = CartBuildAPI(client).create_cart(data=payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'The Metro and The Metro Configuration belong to different facilities.'


class TestGetCart:
    @users(User.SUPERUSER)
    def test_getCartBySuperuser_returns200AndData(self, client, user, request):
        # Act
        response, model = CartBuildAPI(client).get_cart()

        # Assert
        APIResponse(response).assert_status(200)
