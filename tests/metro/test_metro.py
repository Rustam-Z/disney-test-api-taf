from api.requests.metro_api import MetroAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
from tests.fixtures.metro_fixtures import create_fake_metro


class TestMetroCRUD:
    @users(User.SUPERUSER)
    def test_createMetro_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_metro')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

    @users(User.SUPERUSER)
    def test_deleteMetro_byValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_metro')()
        existing_id = model.data.id

        # Act
        response, model = MetroAPI(client).delete_metro(id=existing_id)

        # Assert
        APIResponse(response).assert_status(204)
