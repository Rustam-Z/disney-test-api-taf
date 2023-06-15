from api.endpoints.dashboards.order_history_api import OrderHistoryDashboardAPI
from api.enums.params import Param
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestGetOrderHistory:
    @users(User.SUPERUSER)
    def test_getOrderHistory_withValidData_returns200AndData(self, client, user, create_fake_order_superuser):
        # Arrange
        setup_payload, setup_response, setup_model = create_fake_order_superuser()
        facility_id = setup_model.data.facility

        # Act
        params = {
            Param.FACILITY.value: facility_id
        }
        response, model = OrderHistoryDashboardAPI(client).get_order_history(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model['data']['results']) == 0

    @users(User.SUPERUSER)
    def test_getOrderHistory_withValidData_returns200AndData(self, client, user, deliver_order):
        # Arrange
        facility_id = deliver_order.get('facility_id')

        # Act
        params = {
            Param.FACILITY.value: facility_id
        }
        response, model = OrderHistoryDashboardAPI(client).get_order_history(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model['data']['results']) == 1
        assert model['data']['results'][0]['id'] == deliver_order.get('model')['data']['order_id'], \
            "Order IDs are not matching"


class TestGetOrderHistoryChart:
    @users(User.SUPERUSER)
    def test_getOrderHistoryChart_withValidData_returns200AndData(self, client, user, create_fake_facility):
        # Arrange
        setup_payload, setup_response, setup_model = create_fake_facility()
        facility_id = setup_model.data.id

        # Act
        params = {
            Param.FACILITY.value: facility_id
        }
        response, model = OrderHistoryDashboardAPI(client).get_order_history_chart(params)

        # Assert
        APIResponse(response).assert_status(200)


class TestGetOrderMetros:
    @users(User.SUPERUSER)
    def test_getOrderMetros_withValidData_returns200AndData(self, client, user, assign_metro):
        # Arrange
        setup = assign_metro()
        order_id = setup.get('order_id')

        # Act
        response, model = OrderHistoryDashboardAPI(client).get_order_metros(order_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model['data']) >= 1


class TestGetOrderItemTypes:
    @users(User.SUPERUSER)
    def test_getOrderItemTypes_withValidData_returns200AndData(self, client, user, assign_metro):
        # Arrange
        setup = assign_metro()
        order_id = setup.get('order_id')

        # Act
        response, model = OrderHistoryDashboardAPI(client).get_order_item_types(order_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model['data']) >= 1
