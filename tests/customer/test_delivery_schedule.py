import pytest

import data
from api.endpoints.customer.delivery_schedule_api import DeliveryScheduleAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateDeliverySchedule:
    @users(User.SUPERUSER)
    def test_createDeliverySchedule_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_schedule_superuser')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)


class TestAllDeliverySchedule:
    @users(User.SUPERUSER)
    def test_getAllDeliverySchedules_returns200AndData(self, client, user):
        # Act
        response, model = DeliveryScheduleAPI(client).get_all_schedules()

        # Assert
        APIResponse(response).assert_status(200)
