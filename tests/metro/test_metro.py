from api.endpoints.metro.metro_api import MetroAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateMetro:
    @users(User.SUPERUSER)
    def test_createMetroBySuperuser_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_metro_superuser')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)


class TestDeleteMetro:
    @users(User.SUPERUSER)
    def test_deleteMetroBySuperuser_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_metro_superuser')()
        existing_id = model.data.id

        # Act
        response, model = MetroAPI(client).delete_metro(id=existing_id)

        # Assert
        APIResponse(response).assert_status(204)
