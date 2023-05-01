from datetime import datetime

import pytest

import data
from api.endpoints.customer.customer_api import CustomerAPI
from api.endpoints.order.driver_assignment import DriverAssignmentAPI
from api.enums.params import Param
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestGetUnassignedOrders:
    @users(User.SUPERUSER)
    def test_getUnassignedOrders_withNoOrders_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=1)
        facility_id = model.data.id
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        params = {
            Param.DATE_START_TIME_UTC.value: current_time,
            Param.FACILITY.value: facility_id
        }

        # Act
        response, model = DriverAssignmentAPI(client).get_unassigned_orders(params=params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 0, "Zero orders are expected for facility having no orders."

    @users(User.SUPERUSER)
    def test_getUnassignedOrders_withNotExistingFacility_returns400AndError(self, client, user):
        # Arrange
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        params = {
            Param.DATE_START_TIME_UTC.value: current_time,
            Param.FACILITY.value: data.fake.pyint()  # Not existing facility
        }

        # Act
        response, model = DriverAssignmentAPI(client).get_unassigned_orders(params=params)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'Facility was not found'

    @users(User.SUPERUSER)
    def test_getUnassignedOrders_withExistingOrders_returns200AndData(self, client, user, request):
        # Arrange: create order
        payload, response, model = request.getfixturevalue('create_fake_order_superuser')()
        order_id = model.data.id
        facility_id = model.data.facility
        time = model.data.dropoff_date_start
        params = {
            Param.DATE_START_TIME_UTC.value: time,
            Param.FACILITY.value: facility_id
        }

        # Act
        response, model = DriverAssignmentAPI(client).get_unassigned_orders(params=params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 1, "One order is expected for facility having 1 order."
        assert order_id in [order.id for order in model.data.results]

    @users(User.SUPERUSER)
    def test_getUnassignedOrders_withoutDataStartTimeUTCQueryStringParam_returns400AndError(self, client, user):
        # Arrange
        params = {
            Param.FACILITY.value: data.fake.pyint()  # Not existing facility
        }

        # Act
        response, model = DriverAssignmentAPI(client).get_unassigned_orders(params=params)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'Please, provide date_start_time_utc!'


class TestAssignOrdersToTruckAndDrivers:
    @users(User.SUPERUSER)
    def test_assignOrders_withValidData_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('driver_assignment')
        facility_id = setup.get('facility_id')
        truck_id = setup.get('truck_id')
        driver_id = setup.get('driver_id')
        order_id = setup.get('order_id')
        dropoff_date_start = setup.get('dropoff_date_start')

        # Act
        params = {
            Param.DATE_START_TIME_UTC.value: dropoff_date_start,
            Param.FACILITY.value: facility_id
        }
        payload = data.fake.model.driver_assignment_to_one_order(
            truck=truck_id,
            drivers=[driver_id],
            assigned_orders=[order_id],
            unassigned_orders=[],
        )
        response, model = DriverAssignmentAPI(client).assign_orders_to_truck_and_drivers(params=params, data=payload)

        # Assert
        APIResponse(response).assert_status(200)

    @pytest.mark.skip
    @users(User.SUPERUSER)
    def test_unassignOrders_withValidData_returns200AndData(self, client, user, request):
        ...


class TestGetTruckOrdersAndDrivers:
    @users(User.SUPERUSER)
    def test_getTruckOrdersAndDrivers_withNoAssignedOrders_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('driver_assignment')
        facility_id = setup.get('facility_id')
        truck_id = setup.get('truck_id')
        dropoff_date_start = setup.get('dropoff_date_start')

        # Act
        params = {
            Param.DATE_START_TIME_UTC.value: dropoff_date_start,
            Param.FACILITY.value: facility_id
        }
        response, model = DriverAssignmentAPI(client).get_truck_orders_and_drivers(params=params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data) == 1, 'Only 1 truck is expected to be returned.'
        assert truck_id == model.data[0].id

    @users(User.SUPERUSER)
    def test_getTruckOrdersAndDrivers_withAssignedOrders_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('driver_assignment')
        facility_id = setup.get('facility_id')
        customer_id = setup.get('customer_id')
        truck_id = setup.get('truck_id')
        driver_id = setup.get('driver_id')
        order_id = setup.get('order_id')
        dropoff_date_start = setup.get('dropoff_date_start')
        params = {
            Param.DATE_START_TIME_UTC.value: dropoff_date_start,
            Param.FACILITY.value: facility_id
        }

        # Act: Assign orders to truck and drivers.
        payload = data.fake.model.driver_assignment_to_one_order(
            truck=truck_id,
            drivers=[driver_id],
            assigned_orders=[order_id],
            unassigned_orders=[],
        )
        assignment_response, assignment_model = DriverAssignmentAPI(client).assign_orders_to_truck_and_drivers(params=params, data=payload)
        APIResponse(assignment_response).assert_status(200)

        # Act: Get orders, trucks and drivers.
        response, model = DriverAssignmentAPI(client).get_truck_orders_and_drivers(params=params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data) == 1, 'Only 1 truck is expected to be returned.'
        assert truck_id == model.data[0].id
        assert driver_id == model.data[0].drivers[0].id
        assert facility_id == model.data[0].drivers[0].facility
        assert order_id == model.data[0].orders[0].id

        customer_response, customer_model = CustomerAPI(client).get_customer(id=customer_id)
        assert model.data[0].orders[0].customer_name == customer_model.data.name
