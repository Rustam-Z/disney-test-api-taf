"""
TODO:
- test web CSV upload
- test get metros both mobile and web
- test post metro in mobile
"""
import pytest

from api.endpoints.metro.metro_commission_api import MetroCommissionAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
import data
from fixtures.metro import create_fake_metro_for_commission_superuser


class TestMetroCommissionCRUD:
    @users(User.SUPERUSER)
    def test_createMetro_withSuperUser_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_metro_for_commission_superuser')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

    @pytest.mark.skip(reason="Need to investigate why the test fails.")
    @users(User.FACILITY_ADMIN)
    def test_createMetro_withFacilityAdmin_withValidData_returns201AndData(self, client, user):
        # Arrange
        payload = data.fake.model.metro_for_commission()

        # Act
        response, model = MetroCommissionAPI(client).create_metro(data=payload)

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

    @users(User.SUPERUSER)
    def test_getAllMetros_returns200AndData(self, client, user):
        # Act
        response, model = MetroCommissionAPI(client).get_all_metros()

        # Assert
        APIResponse(response).assert_status(200)
