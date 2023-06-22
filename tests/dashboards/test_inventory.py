from datetime import datetime

import pytest

from api.endpoints.dashboards.inventory_api import InventoryDashboardAPI
from api.enums.params import Param
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestGetCurrentInventory:
    @pytest.mark.parametrize('base_filter, name', [
        ('item_type', 'Item Types'),
        ('metro_config', 'Metro Configurations')
    ])
    @users(User.SUPERUSER)
    def test_getCurrentInventory_withEmptyInventory_returns200AndData(
        self,
        client, user, create_fake_facility,
        base_filter, name
    ):
        # Arrange
        setup_payload, setup_response, setup_model = create_fake_facility()
        facility_id = setup_model.data.id

        # Act
        params = {
            Param.FACILITY.value: facility_id,
            Param.INVENTORY_BASE_FILTER.value: base_filter,
        }
        response, model = InventoryDashboardAPI(client).get_current_inventory(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert model['data']['series'][0]['data'] == [0, 0]
        assert model['data']['series'][0]['name'] == name

    @users(User.SUPERUSER)
    def test_getCurrentInventory_withMetroConfig_returns200AndData(
        self, client, user,
        create_fake_facility,
        create_fake_cart_superuser
    ):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility()
        facility_id = facility_model.data.id
        create_fake_cart_superuser(facility_id=facility_id)

        # Act
        params = {
            Param.FACILITY.value: facility_id,
            Param.INVENTORY_BASE_FILTER.value: 'metro_config',
        }
        response, model = InventoryDashboardAPI(client).get_current_inventory(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert model['data']['series'][0]['data'] == [1, 0]
        assert model['data']['series'][0]['name'] == 'Metro Configurations'

    @users(User.SUPERUSER)
    def test_getCurrentInventory_withItemTypes_returns200AndData(
        self, client, user,
        create_fake_facility,
        create_fake_cart_superuser
    ):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility()
        facility_id = facility_model.data.id
        cart_payload, cart_response, cart_model = create_fake_cart_superuser(facility_id=facility_id)

        # Act
        params = {
            Param.FACILITY.value: facility_id,
            Param.INVENTORY_BASE_FILTER.value: 'item_type',
        }
        response, model = InventoryDashboardAPI(client).get_current_inventory(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert model['data']['series'][0]['name'] == 'Item Types'
        # TODO: Where the number comes from?


class TestGetDailyInventory:
    @pytest.mark.parametrize('daily_inventory_type', ['cart_build', 'delivered'])
    @pytest.mark.parametrize('inventory_base_filter', ['metro_config', 'item_type'])
    @pytest.mark.parametrize('frequency', ['daily', 'weekly', 'monthly'])
    @users(User.SUPERUSER)
    def test_getDailyInventory_withEmptyInventory_returns200AndData(
        self, client, user,
        create_fake_facility,
        daily_inventory_type, inventory_base_filter, frequency
    ):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility()
        facility_id = facility_model.data.id

        # Act
        params = {
            Param.FACILITY.value: facility_id,
            Param.DAILY_INVENTORY_TYPE.value: daily_inventory_type,
            Param.INVENTORY_BASE_FILTER.value: inventory_base_filter,
            Param.FREQUENCY.value: frequency
        }
        response, model = InventoryDashboardAPI(client).get_daily_inventory(params)

        # Assert
        APIResponse(response).assert_status(200)
        assert not all(model['data']['series'][0]['data'])

    @users(User.SUPERUSER)
    def test_getDailyInventory_withCartBuildMetroConfig_returns200AndData(
        self, client, user,
        create_fake_facility,
        create_fake_cart_superuser
    ):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility()
        facility_id = facility_model.data.id
        create_fake_cart_superuser(facility_id=facility_id)

        # Act
        params = {
            Param.FACILITY.value: facility_id,
            Param.DAILY_INVENTORY_TYPE.value: 'cart_build',
            Param.INVENTORY_BASE_FILTER.value: 'metro_config',
            Param.FREQUENCY.value: 'daily'
        }
        response, model = InventoryDashboardAPI(client).get_daily_inventory(params)

        # Assert
        APIResponse(response).assert_status(200)

        last_date = model['data']['dates'][-1]
        given_datetime = datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        current_datetime = datetime.utcnow()
        assert (given_datetime.date() == current_datetime.date() and
                given_datetime.hour == current_datetime.hour and
                given_datetime.minute == current_datetime.minute), "The date, hour, or minutes are not the same."
        assert model['data']['series'][0]['data'][-1] == 1

    @users(User.SUPERUSER)
    def test_getDailyInventory_withDeliveredMetroConfig_returns200AndData(
        self, client, user,
        deliver_order
    ):
        # Arrange
        facility_id = deliver_order.get('facility_id')

        # Act
        params = {
            Param.FACILITY.value: facility_id,
            Param.DAILY_INVENTORY_TYPE.value: 'delivered',
            Param.INVENTORY_BASE_FILTER.value: 'metro_config',
            Param.FREQUENCY.value: 'daily'
        }
        response, model = InventoryDashboardAPI(client).get_daily_inventory(params)

        # Assert
        APIResponse(response).assert_status(200)
        last_date = model['data']['dates'][-1]
        given_datetime = datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        current_datetime = datetime.utcnow()
        assert (given_datetime.date() == current_datetime.date() and
                given_datetime.hour == current_datetime.hour and
                given_datetime.minute == current_datetime.minute), "The date, hour, or minutes are not the same."
        assert model['data']['series'][0]['data'][-1] == 1


class TestGetDailyGoals:
    @users(User.SUPERUSER)
    def test_getDailyGoals_withValidData_returns200AndData(self, client, user):
        ...


class TestGetMetroLocations:
    @users(User.SUPERUSER)
    def test_getMetroLocations_withValidData_returns200AndData(self, client, user):
        ...
