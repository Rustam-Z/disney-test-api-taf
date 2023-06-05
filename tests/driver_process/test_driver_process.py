import random
from datetime import datetime

import pytest

import data
from api.endpoints.driver_process.driver_process_api import DriverProcessAPI
from api.endpoints.metro.metro_api import MetroAPI
from api.endpoints.order.order_api import OrderAPI
from api.enums.metro import MetroProcessStatuses, MetroLaundryStatuses
from api.enums.order import OrderStatuses
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestGetOrders:
    @users(User.SUPERUSER)
    def test_getOrders_withValidDataAndNoOrders_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('driver_assignment')
        driver_id = setup.get('driver_id')

        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        params = {
            'action': 'pickup_at_facility',
            'date_start_time_utc': current_time,
            'driver_id': driver_id,
        }

        # Act
        response, model = DriverProcessAPI(client).get_orders(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 0

    @pytest.mark.skip(reason="From where the order is being fetched?")
    @users(User.SUPERUSER)
    def test_getOrders_withValidDataAndExistingOrders_returns200AndData(self, client, user, request):
        # Arrange
        driver_assignment_setup = request.getfixturevalue('assign_orders_to_truck_and_drivers')
        facility_id = driver_assignment_setup.get('facility_id')
        customer_id = driver_assignment_setup.get('customer_id')
        driver_id = driver_assignment_setup.get('driver_id')
        staging_setup = request.getfixturevalue('staging')(facility_id=facility_id, customer_id=customer_id)
        dropoff_date_start = staging_setup.get('dropoff_date_start')

        params = {
            'action': 'pickup_at_facility',
            'date_start_time_utc': dropoff_date_start,
            'driver_id': driver_id,
        }

        # Act
        response, model = DriverProcessAPI(client).get_orders(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 1

    @users(User.SUPERUSER)
    def test_getOrders_withWrongDriver_returns400AndError(self, client, user):
        # Arrange
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        params = {
            'action': 'pickup_at_facility',
            'date_start_time_utc': current_time,
            'driver_id': data.fake.pyint(),
        }

        # Act
        response, model = DriverProcessAPI(client).get_orders(params)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'Driver Not Found'


class TestGetMetroList:
    @users(User.SUPERUSER)
    def test_getMetroList_withValidData_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('staging')
        order_id = setup.get('order_id')

        # Act
        response, model = DriverProcessAPI(client).get_metro_list(order_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 1

    @users(User.SUPERUSER)
    def test_getMetroList_withWrongOrderID_returns400AndError(self, client, user):
        # Arrange
        order_id = data.fake.pyint()

        # Act
        response, model = DriverProcessAPI(client).get_metro_list(order_id)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'Order Not Found'


class TestReaderMetroScan:
    @users(User.SUPERUSER)
    def test_readerMetroScan_withValidData_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('staging')
        metro_qr_code = setup.get('metro_qr_code')
        metro_id = setup.get('metro_id')
        order_id = setup.get('order_id')

        payload = {
            "reader_name": f"Reader: {data.fake.ean13()}",
            "mac_address": f"192.168.0.{random.randint(0, 255)}",
            "tag_reads": [
                {
                    "antennaPort": random.randint(1, 9),
                    "epc": metro_qr_code
                }
            ]
        }

        # Act
        response, model = DriverProcessAPI(client).reader_metro_scan(payload)

        # Assert
        APIResponse(response).assert_status(200)

        # Act
        metro_response, metro_model = MetroAPI(client).get_metro(metro_id)

        # Assert: Metro status should be changed.
        assert metro_model.data.process_status == MetroProcessStatuses.READY_FOR_DELIVERY.value

        # Act
        order_response, order_model = OrderAPI(client).get_order(order_id)

        # Assert
        assert order_model.data.status == OrderStatuses.READY_FOR_DELIVERY.value


class TestDriverMetroScan:
    @users(User.SUPERUSER)
    def test_driverMetroScan_withValidData_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('staging')
        order_id = setup.get('order_id')
        metro_qr_code = setup.get('metro_qr_code')
        metro_id = setup.get('metro_id')

        payload = {
            "order_id": order_id,
            "qr_code": metro_qr_code
        }

        # Act
        response, model = DriverProcessAPI(client).driver_metro_scan(payload)

        # Assert
        APIResponse(response).assert_status(200)

        # Act
        metro_response, metro_model = MetroAPI(client).get_metro(metro_id)

        # Assert: Metro status should be changed.
        assert metro_model.data.process_status == MetroProcessStatuses.OUT_FOR_DELIVERY.value


class TestSubmit:
    @users(User.SUPERUSER)
    def test_submit_withValidData_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('staging')
        order_id = setup.get('order_id')
        metro_id = setup.get('metro_id')
        metro_qr_code = setup.get('metro_qr_code')

        # Reader metro scan.
        payload = {
            "reader_name": f"Reader: {data.fake.ean13()}",
            "mac_address": f"192.168.0.{random.randint(0, 255)}",
            "tag_reads": [
                {
                    "antennaPort": random.randint(1, 9),
                    "epc": metro_qr_code
                }
            ]
        }
        DriverProcessAPI(client).reader_metro_scan(payload)

        # Driver metro scan.
        payload = {
            "order_id": order_id,
            "qr_code": metro_qr_code
        }
        DriverProcessAPI(client).driver_metro_scan(payload)

        payload = {
            "order_id": order_id
        }

        # Act
        response, model = DriverProcessAPI(client).submit(payload)

        # Assert
        APIResponse(response).assert_status(200)

        # Act
        metro_response, metro_model = MetroAPI(client).get_metro(metro_id)

        # Assert: Metro status should be changed.
        assert metro_model.data.process_status == MetroProcessStatuses.DELIVERED.value
        assert metro_model.data.laundry_status == MetroLaundryStatuses.CLEAN.value
