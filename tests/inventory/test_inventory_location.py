import pytest

import data
from api.endpoints.inventory.inventory_location_api import InventoryLocationAPI
from api.enums.errors import ErrorDetail
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateInventoryLocation:
    @pytest.mark.parametrize('location_type', ['exit', 'clear_metro', 'enter'])
    @users(User.SUPERUSER)
    def test_createInventoryLocation_withValidData_returns201AndData(self, client, user, request, location_type):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_inventory_location_superuser')(
            location_type=location_type
        )

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)
        assert model.data.type == location_type

    @users(User.SUPERUSER)
    def test_createInventoryLocation_withWrongData_returns400AndError(self, client, user):
        # Arrange
        wrong_location_type = data.fake.pystr()

        # Act
        payload = data.fake.model.inventory_location(location_type=wrong_location_type)
        response, model = InventoryLocationAPI(client).create_inventory_location(data=payload)

        # Assert
        APIResponse(response).assert_status(400)


class TestGetAllInventoryLocations:
    @users(User.SUPERUSER)
    def test_getAllInventoryLocations_returns200AndData(self, client, user):
        # Act
        response, model = InventoryLocationAPI(client).get_all_inventory_locations()

        # Assert
        APIResponse(response).assert_status(200)


class TestGetInventoryLocation:
    @users(User.SUPERUSER)
    def test_getInventoryLocation_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_inventory_location_superuser')()
        inventory_location_id = model.data.id

        # Act
        response, model = InventoryLocationAPI(client).get_inventory_location(id=inventory_location_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == inventory_location_id
        APIResponse(response).assert_models(payload)


class TestUpdateInventoryLocation:
    @users(User.SUPERUSER)
    def test_updateInventoryLocation_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_inventory_location_superuser')()
        inventory_location_id = model.data.id
        facility_id = model.data.facility

        # Act
        payload = data.fake.model.inventory_location(facility_id=facility_id)
        response, model = InventoryLocationAPI(client).update_inventory_location(id=inventory_location_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        APIResponse(response).assert_models(payload)
        assert inventory_location_id == model.data.id


class TestDeleteOrder:
    @users(User.SUPERUSER)
    def test_deleteInventoryLocation_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_inventory_location_superuser')()
        inventory_location_id = model.data.id

        # Act
        response, response_payload = InventoryLocationAPI(client).delete_inventory_location(id=inventory_location_id)

        # Assert
        APIResponse(response).assert_status(204)

        # Act: Remove already removed object.
        response, model = InventoryLocationAPI(client).delete_inventory_location(id=inventory_location_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == ErrorDetail.NOT_FOUND.value
