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


class TestAssignMetro:
    @users(User.SUPERUSER)
    def test_assignMetro_withValidData_returns200AndData(self, client, user, request):
        # Arrange: create order, assign metros
        order_payload, order_response, order_model = request.getfixturevalue('create_fake_order_superuser')()
        facility_id = order_model.data.facility
        order_id = order_model.data.id

        cart_payload, cart_response, cart_model = request.getfixturevalue('create_fake_cart_superuser')(
            facility_id=facility_id
        )
        metro_qr_code = cart_model['data']['metro']['qr_code']

        # Act
        payload = {
            "metro_qr_code": metro_qr_code,
            "order_id": order_id
        }
        response, model = StagingAPI(client).assign_metro(payload)

        # Assert
        APIResponse(response).assert_status(200)
        assert model['data']['order_id'] == order_id
        assert model['data']['metro_qr_code'] == metro_qr_code

    @users(User.SUPERUSER)
    def test_assignMetro_withMetroWithoutCartBuild_returns400AndError(self, client, user, request):
        # Arrange
        order_payload, order_response, order_model = request.getfixturevalue('create_fake_order_superuser')()
        facility_id = order_model.data.facility
        order_id = order_model.data.id

        metro_payload, metro_response, metro_model = request.getfixturevalue('create_fake_metro_superuser')(
            facility_id=facility_id
        )
        metro_qr_code = metro_model.data.qr_code

        # Act
        payload = {
            "metro_qr_code": metro_qr_code,
            "order_id": order_id
        }
        response, model = StagingAPI(client).assign_metro(payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'There is no cart build with this metro!'

    @users(User.SUPERUSER)
    def test_assignMetro_withWrongMetro_returns400AndError(self, client, user, request):
        # Arrange
        order_payload, order_response, order_model = request.getfixturevalue('create_fake_order_superuser')()
        order_id = order_model.data.id
        metro_qr_code = data.fake.pyint()

        # Act
        payload = {
            "metro_qr_code": metro_qr_code,
            "order_id": order_id
        }
        response, model = StagingAPI(client).assign_metro(payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'There is no metro with this qr code!'


class TestRemoveMetro:
    @users(User.SUPERUSER)
    def test_removeMetro_withValidData_returns200AndData(self, client, user, request):
        # Arrange: create order, assign metros
        setup = request.getfixturevalue('assign_metro')()
        cart_id = setup.get('cart_id')
        order_id = setup.get('order_id')

        # Act
        payload = {
            "cart_build_id": cart_id,
            "order_id": order_id
        }
        response, model = StagingAPI(client).remove_metro(payload)

        # Assert
        APIResponse(response).assert_status(200)
        assert model['data']['message'] == 'Metro Removed successfully'


class TestGetMetroList:
    @users(User.SUPERUSER)
    def test_getMetroList_withExistingOrderAndNoMetros_returns200AndData(self, client, user, request):
        # Arrange: create order, assign metros
        order_payload, order_response, order_model = request.getfixturevalue('create_fake_order_superuser')()
        order_id = order_model.data.id
        params = {
            Param.ORDER_ID.value: order_id
        }

        # Act
        response, model = StagingAPI(client).get_metro_list(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 0, "No metros should be associated with order."

    @users(User.SUPERUSER)
    def test_getMetroList_withExistingOrderAndWithMetros_returns200AndData(self, client, user, request):
        # Arrange: create order, assign metros
        setup = request.getfixturevalue('assign_metro')()
        cart_id = setup.get('cart_id')
        order_id = setup.get('order_id')
        metro_qr_code = setup.get('metro_qr_code')

        # Act
        params = {
            Param.ORDER_ID.value: order_id
        }
        response, model = StagingAPI(client).get_metro_list(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 1
        assert model.data.results[0].metro_qr_code == metro_qr_code
        assert model.data.results[0].cart_build_id == cart_id

    @users(User.SUPERUSER)
    def test_getMetroList_withWrongOrder_returns400AndError(self, client, user):
        # Arrange: create order, assign metros
        params = {
            Param.ORDER_ID.value: data.fake.pyint()
        }

        # Act
        response, model = StagingAPI(client).get_metro_list(params)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == 'Order Not Found'


class TestSubmitAction:
    @users(User.SUPERUSER)
    def test_submitAction_withValidData_returns200AndData(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('assign_metro')()
        customer_id = setup.get('customer_id')
        order_id = setup.get('order_id')
        customer_response, customer_model = CustomerAPI(client).get_customer(customer_id)
        customer_barcode = customer_model.data.barcode

        # Act
        payload = {
            "order_id": order_id,
            "disney_order_id": data.fake.pyint(),
            "customer_barcode": customer_barcode
        }
        response, model = StagingAPI(client).submit_action(payload)

        # Assert
        APIResponse(response).assert_status(200)

    @users(User.SUPERUSER)
    def test_submitAction_withDifferentCustomerBarcode_returns400AndError(self, client, user, request):
        # Arrange: create order, assign metros
        order_payload, order_response, order_model = request.getfixturevalue('create_fake_order_superuser')()
        order_id = order_model.data.id

        # Act
        payload = {
            "order_id": order_id,
            "disney_order_id": data.fake.ean(),
            "customer_barcode": data.fake.ean()
        }
        response, model = StagingAPI(client).submit_action(payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('detail') == "Provided barcode is not the same with order's customer barcode. Please check it!"

    @users(User.SUPERUSER)
    def test_submitAction_withLongDisneyOrderID_returns400AndError(self, client, user, request):
        # Arrange
        setup = request.getfixturevalue('assign_metro')()
        customer_id = setup.get('customer_id')
        order_id = setup.get('order_id')
        customer_response, customer_model = CustomerAPI(client).get_customer(customer_id)
        customer_barcode = customer_model.data.barcode

        # Act
        payload = {
            "order_id": order_id,
            "disney_order_id": data.fake.ean(),
            "customer_barcode": customer_barcode
        }
        response, model = StagingAPI(client).submit_action(payload)

        # Assert
        APIResponse(response).assert_status(400)
