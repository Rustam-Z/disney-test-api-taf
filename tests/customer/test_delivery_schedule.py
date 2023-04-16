import pytest

import data
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
