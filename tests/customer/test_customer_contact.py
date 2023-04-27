import pytest

import data
from api.endpoints.customer.customer_contact_api import CustomerContactAPI
from api.enums.errors import ErrorDetail
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateCustomerContact:
    @users(User.SUPERUSER)
    def test_createCustomerContact_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_customer_contact')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)


class TestGetAllCustomerContacts:
    @users(User.SUPERUSER)
    def test_getAllCustomerContacts_returns200AndData(self, client, user):
        # Act
        response, model = CustomerContactAPI(client).get_all_customer_contacts()

        # Assert
        APIResponse(response).assert_status(200)


class TestGetCustomerContact:
    @users(User.SUPERUSER)
    def test_getCustomerContact_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_customer_contact')()
        customer_contact_id = model.data.id

        # Act
        response, model = CustomerContactAPI(client).get_customer_contact(id=customer_contact_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == customer_contact_id
        APIResponse(response).assert_models(payload)


class TestUpdateCustomerContact:
    @users(User.SUPERUSER)
    def test_updateCustomerContact_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_customer_contact')()
        customer_contact_id = model.data.id
        facility_id = model.data.facility
        customer_id = model.data.customer

        # Act
        payload = data.fake.model.delivery_schedule(facility_id=facility_id, customer_id=customer_id)
        response, model = CustomerContactAPI(client).update_customer_contact(id=customer_contact_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        APIResponse(response).assert_models(payload)
        assert customer_contact_id == model.data.id


class TestCustomerContact:
    @users(User.SUPERUSER)
    def test_deleteCustomerContact_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_customer_contact')()
        customer_contact_id = model.data.id

        # Act
        response, response_payload = CustomerContactAPI(client).delete_customer_contact(id=customer_contact_id)

        # Assert
        APIResponse(response).assert_status(204)

        # Act: Remove already removed object.
        response, model = CustomerContactAPI(client).delete_customer_contact(id=customer_contact_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == ErrorDetail.NOT_FOUND.value
