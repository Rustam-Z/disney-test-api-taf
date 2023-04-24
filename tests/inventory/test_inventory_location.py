import pytest

import data
from api.endpoints.order.order_api import OrderAPI
from api.enums.errors import ErrorDetail
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateOrder:
    @users(User.SUPERUSER)
    def test_createOrder_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_order')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)


class TestGetAllOrders:
    @users(User.SUPERUSER)
    def test_getAllOrders_returns200AndData(self, client, user):
        # Act
        response, model = OrderAPI(client).get_all_orders()

        # Assert
        APIResponse(response).assert_status(200)


class TestGetOrder:
    @users(User.SUPERUSER)
    def test_getOrder_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_order')()
        order_id = model.data.id

        # Act
        response, model = OrderAPI(client).get_order(id=order_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == order_id
        APIResponse(response).assert_models(payload)


class TestUpdateOrder:
    @users(User.SUPERUSER)
    def test_updateOrder_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_order')()
        order_id = model.data.id
        facility_id = model.data.facility
        customer_id = model.data.customer

        # Act
        payload = data.fake.model.order(facility_id=facility_id, customer_id=customer_id)
        response, model = OrderAPI(client).update_order(id=order_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        APIResponse(response).assert_models(payload)
        assert order_id == model.data.id


class TestDeleteOrder:
    @users(User.SUPERUSER)
    def test_deleteOrder_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_order')()
        order_id = model.data.id

        # Act
        response, response_payload = OrderAPI(client).delete_order(id=order_id)

        # Assert
        APIResponse(response).assert_status(204)

        # Act: Remove already removed object.
        response, model = OrderAPI(client).delete_order(id=order_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == ErrorDetail.NOT_FOUND.value
