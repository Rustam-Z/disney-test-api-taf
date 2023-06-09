import data
from api.endpoints.metro.cart_build_api import CartBuildAPI
from api.endpoints.metro.metro_api import MetroAPI
from api.enums.metro import MetroProcessStatuses, MetroLaundryStatuses
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateCart:
    @users(User.SUPERUSER)
    def test_createCart_withValidData_returns200AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_cart_superuser')()
        metro_id = model.data.metro.id

        # Assert
        APIResponse(response).assert_status(200)

        # Act
        metro_response, metro_model = MetroAPI(client).get_metro(metro_id)

        # Assert
        assert metro_model.data.process_status == MetroProcessStatuses.STAGED_IN_INVENTORY.value
        assert metro_model.data.laundry_status == MetroLaundryStatuses.CLEAN.value

    @users(User.SUPERUSER)
    def test_createCart_withMetroAndMetroConfigBelongingToDifferentFacility_returns400AndError(self, client, user, request):
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

    @users(User.SUPERUSER)
    def test_cartRebuild_withValidData_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_cart_superuser')()
        metro_qr_code = model.data.metro.qr_code
        metro_config_qr_code = model.data.metro_config.qr_code

        # Act
        payload = data.fake.model.cart(
            metro_qr_code=metro_qr_code,
            metro_config_qr_code=metro_config_qr_code,
            is_rebuild=True
        )
        response, model = CartBuildAPI(client).rebuild_cart(data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.get('data').get('is_rebuild') is True

    @users(User.SUPERUSER)
    def test_cartRebuild_afterStaging_returns400AndError(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('staging')
        metro_qr_code = setup.get('metro_qr_code')
        metro_config_qr_code = setup.get('metro_config_qr_code')

        # Act
        payload = data.fake.model.cart(
            metro_qr_code=metro_qr_code,
            metro_config_qr_code=metro_config_qr_code,
            is_rebuild=True
        )
        response, model = CartBuildAPI(client).create_cart(data=payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == "Metro is already staged."


class TestGetCart:
    @users(User.SUPERUSER)
    def test_getCartBySuperuser_returns200AndData(self, client, user, request):
        # Arrange
        request.getfixturevalue('create_fake_cart_superuser')()

        # Act
        response, model = CartBuildAPI(client).get_cart()

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) > 0
