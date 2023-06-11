import random

import data
from api.endpoints.customer.customer_contact_api import CustomerContactAPI
from api.enums.errors import ErrorDetail
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateCustomerContact:
    @users(User.SUPERUSER)
    def test_createCustomerContact_withValidData_returns201AndData(self, client, user, create_fake_facility):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
        facility_id = facility_model.data.id
        customer_id = random.choice(facility_model.data.customers)

        # Act
        payload = data.fake.model.customer_contact(facility_id=facility_id, customer_id=customer_id)
        response, model = CustomerContactAPI(client).create_customer_contact(data=payload)

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

    @users(User.SUPERUSER)
    def test_createCustomerContact_withWrongCustomer_returns400AndError(self, client, user, create_fake_facility):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
        facility_id = facility_model.data.id
        customer_id = data.fake.ean()

        # Act
        payload = data.fake.model.customer_contact(facility_id=facility_id, customer_id=customer_id)
        response, model = CustomerContactAPI(client).create_customer_contact(data=payload)

        # Assert
        APIResponse(response).assert_status(400)


class TestGetAllCustomerContacts:
    @users(User.SUPERUSER)
    def test_getAllCustomerContacts_returns200AndData(
        self, client, user, create_fake_customer_contact_superuser
    ):
        # Arrange
        create_fake_customer_contact_superuser()

        # Act
        response, model = CustomerContactAPI(client).get_all_customer_contacts()

        # Assert
        APIResponse(response).assert_status(200)
        assert len(model.data.results) >= 1


class TestGetCustomerContact:
    @users(User.SUPERUSER)
    def test_getCustomerContact_withValidID_returns200AndData(
        self, client, user, create_fake_customer_contact_superuser
    ):
        # Arrange
        payload, response, model = create_fake_customer_contact_superuser()
        customer_contact_id = model.data.id

        # Act
        response, model = CustomerContactAPI(client).get_customer_contact(id=customer_contact_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == customer_contact_id
        APIResponse(response).assert_models(payload)


class TestUpdateCustomerContact:
    @users(User.SUPERUSER)
    def test_updateCustomerContact_withValidID_returns200AndData(
        self, client, user, create_fake_customer_contact_superuser
    ):
        # Arrange
        payload, response, model = create_fake_customer_contact_superuser()
        customer_contact_id = model.data.id
        facility_id = model.data.facility
        customer_id = model.data.customer

        # Act
        payload = data.fake.model.customer_contact(facility_id=facility_id, customer_id=customer_id)
        response, model = CustomerContactAPI(client).update_customer_contact(id=customer_contact_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        APIResponse(response).assert_models(payload)
        assert customer_contact_id == model.data.id

    @users(User.SUPERUSER)
    def test_updateCustomerContact_withWrongID_returns404AndError(self, client, user):
        # Arrange
        customer_contact_id = data.fake.pyint()
        facility_id = data.fake.pyint()
        customer_id = data.fake.pyint()

        # Act
        payload = data.fake.model.customer_contact(facility_id=facility_id, customer_id=customer_id)
        response, model = CustomerContactAPI(client).update_customer_contact(id=customer_contact_id, data=payload)

        # Assert
        APIResponse(response).assert_status(404)


class TestDeleteCustomerContact:
    @users(User.SUPERUSER)
    def test_deleteCustomerContact_withValidID_returns204(
        self, client, user, create_fake_customer_contact_superuser
    ):
        # Arrange
        payload, response, model = create_fake_customer_contact_superuser()
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

    @users(User.SUPERUSER)
    def test_deleteCustomerContact_withWrongID_returns204(self, client, user):
        # Arrange
        customer_contact_id = data.fake.pyint()

        # Act
        response, model = CustomerContactAPI(client).delete_customer_contact(id=customer_contact_id)

        # Assert
        APIResponse(response).assert_status(404)
