from api.endpoints.user.drivers_list import DriversListAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestGetAllDrivers:
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_getAllDrivers_return200AndData(self, client, user):
        # Act
        response, model = DriversListAPI(client).get_drivers_list()

        # Assert
        APIResponse(response).assert_status(200)

    @users(User.FACILITY_ADMIN)
    def test_getAllDrivers_withExistingDrivers_return200AndData(self, client, user, request):
        # Arrange
        request.getfixturevalue('create_fake_role')(is_driver=True)

        # Act
        response, model = DriversListAPI(client).get_drivers_list()

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 1
