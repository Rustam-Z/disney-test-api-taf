import pytest

import data
from api.endpoints.customer.delivery_schedule_api import DeliveryScheduleAPI
from api.enums.errors import ErrorDetail
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


class TestUpdateDeliverySchedule:
    @users(User.SUPERUSER)
    def test_updateDeliverySchedule_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_schedule_superuser')()
        delivery_schedule_id = model.data.id
        facility_id = model.data.facility
        customer_id = model.data.customer

        # Act
        payload = data.fake.model.delivery_schedule(facility_id=facility_id, customer_id=customer_id)
        response, model = DeliveryScheduleAPI(client).update_schedule(id=delivery_schedule_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        APIResponse(response).assert_models(payload)
        assert delivery_schedule_id == model.data.id


class TestDeleteDeliverySchedule:
    @users(User.SUPERUSER)
    def test_deleteDeliverySchedule_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_schedule_superuser')()
        delivery_schedule_id = model.data.id

        # Act
        response, response_payload = DeliveryScheduleAPI(client).delete_schedule(id=delivery_schedule_id)

        # Assert
        APIResponse(response).assert_status(204)

        # Act: Remove already removed object.
        response, model = DeliveryScheduleAPI(client).delete_schedule(id=delivery_schedule_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == ErrorDetail.NOT_FOUND.value
