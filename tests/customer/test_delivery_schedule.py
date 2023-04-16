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


class TestGetAllDeliverySchedule:
    @users(User.SUPERUSER)
    def test_getAllDeliverySchedules_returns200AndData(self, client, user):
        # Act
        response, model = DeliveryScheduleAPI(client).get_all_schedules()

        # Assert
        APIResponse(response).assert_status(200)


class TestGetDeliverySchedule:
    @users(User.SUPERUSER)
    def test_getDeliverySchedule_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_schedule_superuser')()
        delivery_schedule_id = model.data.id

        # Act
        response, model = DeliveryScheduleAPI(client).get_schedule(id=delivery_schedule_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == delivery_schedule_id
        APIResponse(response).assert_models(payload)

