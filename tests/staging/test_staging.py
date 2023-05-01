from datetime import datetime

import pytest

import data
from api.endpoints.customer.customer_api import CustomerAPI
from api.endpoints.staging.staging_api import StagingAPI
from api.enums.params import Param
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestGetOrders:
    @users(User.SUPERUSER)
    def test_getOrders_forAllFacilities_returns200AndData(self, client, user):
        # Act
        response, model = StagingAPI(client).get_orders()

        # Assert
        APIResponse(response).assert_status(200)

    @users(User.SUPERUSER)
    def test_getOrders_forFacilityWithNoOrders_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=1)
        facility_id = model.data.id

        params = {
            Param.FACILITY.value: facility_id
        }

        # Act
        response, model = StagingAPI(client).get_orders(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 0

    @users(User.SUPERUSER)
    def test_getOrders_forFacilityWithExistingOrder_returns200AndData(self, client, user, request):
        # Arrange
        order_payload, order_response, order_model = request.getfixturevalue('create_fake_order_superuser')()
        facility_id = order_model.data.facility
        customer_id = order_model.data.customer
        params = {
            Param.FACILITY.value: facility_id
        }

        # Act
        response, model = StagingAPI(client).get_orders(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 1
        assert model.data.results[0].unique_id == order_model.data.unique_id

        customer_response, customer_model = CustomerAPI(client).get_customer(id=customer_id)
        assert model.data.results[0].customer_name == customer_model.data.name

    @users(User.SUPERUSER)
    def test_getOrders_forFacilityWithInvalidFacility_returns400AndError(self, client, user):
        # Arrange
        params = {
            Param.FACILITY.value: data.fake.pyint()
        }

        # Act
        response, model = StagingAPI(client).get_orders(params)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'Facility was not found'

    @pytest.mark.skip
    @users(User.SUPERUSER)
    def test_getOrders_forFacilityByCustomer_returns200AndData(self, client, user):
        # Arrange
        params = {
            Param.FACILITY.value: ...,
            Param.CUSTOMER_BARCODE.value: ...
        }

        # Act
        response, model = StagingAPI(client).get_orders(params)

        # Assert
        APIResponse(response).assert_status(200)


class TestGetMetrosList:
    ...


class TestAssignMetro:
    ...


class TestRemoveMetro:
    ...


class TestSubmitAction:
    ...


class TestGetMetroItemConfigDetail:
    ...
