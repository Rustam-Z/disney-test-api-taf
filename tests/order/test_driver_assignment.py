from datetime import datetime
import random

import data
from api.endpoints.order.driver_assignment import DriverAssignmentAPI
from api.enums.params import Param
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestGetUnassignedOrders:
    @users(User.SUPERUSER)
    def test_getUnassignedOrders_withNoOrders_returns200AndData(self, client, user):
        # Arrange
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        params = {
            Param.DATE_START_TIME_UTC.value: current_time,
            Param.FACILITY.value: data.fake.pyint()  # Not existing facility
        }

        # Act
        response, model = DriverAssignmentAPI(client).get_unassigned_orders(params=params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 0, "Zero orders are expected for facility having no orders."

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


class TestAssignDriverAndOrder:
    @users(User.SUPERUSER)
    def test_assignDriverAndOrder_withValidData_returns200AndData(self, client, user, request):
        ...


class TestGetTruckOrdersAndDrivers:
    @users(User.SUPERUSER)
    def test_getTruckOrdersAndDrivers_withNoAssignedOrdersToTruckAndDriver_returns200AndData(self, client, user, request):
        # Arrange: create facility, drivers, truck, orders.

        # Create facility
        facility_payload, facility_response, facility_model = request.getfixturevalue('create_fake_facility')(no_of_customers=2)
        facility_id = facility_model.data.id
        customer_id = random.choice(facility_model.data.customers)

        # Create driver
        driver_payload, driver_response, driver_model = request.getfixturevalue('create_fake_role')(
            is_driver=True, facility_id=facility_id
        )
        driver_id = driver_model.data.id
        assert driver_model.data.facility == facility_id

        # Create truck
        truck_payload, truck_response, truck_model = request.getfixturevalue('create_fake_truck_superuser')(
            facility_id=facility_id
        )
        truck_id = truck_model.data.id
        assert truck_model.data.facility == facility_id

        # Create orders
        order_payload, order_response, order_model = request.getfixturevalue('create_fake_order_superuser')(
            facility_id=facility_id,
            customer_id=customer_id
        )
        order_id = order_model.data.id
        assert order_model.data.facility == facility_id
        assert order_model.data.customer == customer_id

        time = order_model.data.dropoff_date_start
        params = {
            Param.DATE_START_TIME_UTC.value: time,
            Param.FACILITY.value: facility_id
        }

        # Act
        response, model = DriverAssignmentAPI(client).get_truck_orders_and_drivers(params=params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data) == 1, 'Only 1 truck is expected to be returned.'
        assert truck_id == model.data[0].id
