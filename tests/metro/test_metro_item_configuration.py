from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
import data
from api.endpoints.metro.metro_item_configuration_api import MetroItemConfigurationAPI
from fixtures.metro_item_configuration import create_fake_metro_item_configuration_superuser


class TestMetroItemConfigurationCRUD:
    @users(User.SUPERUSER)
    def test_createMetroItemConfig_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_metro_item_configuration_superuser')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

    @users(User.SUPERUSER)
    def test_deleteMetroItemConfig_byValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_metro_item_configuration_superuser')()
        existing_id = model.data.id

        # Act
        response, model = MetroItemConfigurationAPI(client).delete_config(id=existing_id)

        # Assert
        APIResponse(response).assert_status(204)

    @users(User.SUPERUSER)
    def test_deleteMetroItemConfig_byValidID_returns404(self, client, user, request):
        # Arrange
        not_existing_id = data.fake.uuid4()

        # Act
        response, model = MetroItemConfigurationAPI(client).delete_config(id=not_existing_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == 'Not found.'
