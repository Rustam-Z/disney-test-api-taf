import data
from api.endpoints.metro.metro_api import MetroAPI
from api.enums.metro import MetroProcessStatuses, MetroLaundryStatuses
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateMetro:
    @users(User.SUPERUSER)
    def test_createMetroBySuperuser_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_metro_superuser')()
        metro_id = model.data.id

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)
        assert model.data.process_status == MetroProcessStatuses.STAGED_IN_INVENTORY.value
        assert model.data.laundry_status == MetroLaundryStatuses.NONE.value

        # Act
        response, model = MetroAPI(client).get_metro(metro_id)

        # Assert
        APIResponse(response).assert_status(200)
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

    @users(User.SUPERUSER)
    def test_deleteMetroBySuperuser_withWrongID_returns404(self, client, user):
        # Arrange
        not_existing_id = data.fake.pyint()

        # Act
        response, model = MetroAPI(client).delete_metro(id=not_existing_id)

        # Assert
        APIResponse(response).assert_status(404)
