import pytest

import data
from api.endpoints.facility.truck_api import TruckAPI
from api.enums.errors import ErrorDetail
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateTruck:
    @users(User.SUPERUSER)
    def test_createTruck_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_truck')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)


class TestGetAllTrucks:
    @users(User.SUPERUSER)
    def test_getAllTrucks_returns200AndData(self, client, user):
        # Act
        response, model = TruckAPI(client).get_all_trucks()

        # Assert
        APIResponse(response).assert_status(200)


class TestGetTruck:
    @users(User.SUPERUSER)
    def test_getTruck_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_truck')()
        truck_id = model.data.id

        # Act
        response, model = TruckAPI(client).get_truck(id=truck_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == truck_id
        APIResponse(response).assert_models(payload)


class TestUpdateTruck:
    @users(User.SUPERUSER)
    def test_updateTruck_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_truck')()
        truck_id = model.data.id
        facility_id = model.data.facility

        # Act
        payload = data.fake.model.truck(facility_id=facility_id)
        response, model = TruckAPI(client).update_truck(id=truck_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        APIResponse(response).assert_models(payload)
        assert truck_id == model.data.id


class TestDeleteTruck:
    @users(User.SUPERUSER)
    def test_deleteTruck_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_truck')()
        truck_id = model.data.id

        # Act
        response, response_payload = TruckAPI(client).delete_truck(id=truck_id)

        # Assert
        APIResponse(response).assert_status(204)

        # Act: Remove already removed object.
        response, model = TruckAPI(client).delete_truck(id=truck_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == ErrorDetail.NOT_FOUND.value
