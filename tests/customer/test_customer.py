"""
Test customer CRUD.
"""
import pytest

from api.requests.customer_api import CustomerAPI
from api.responses.common_models import UnauthRequestErrorResponse
from core.api_response import APIResponse
from core.decorators import users
from core.enums.users import User
import data


class TestCustomer:
    @users(User.SUPERUSER)
    def test_createNewCustomer_returns201AndData(self, client, user):
        # Act and assert
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).create_customer(data=payload)
        APIResponse(response).check_status(201)
        assert payload['name'] == model.data.name
        assert payload['barcode'] == model.data.barcode

        # Cleanup
        CustomerAPI(client).delete_customer(id=model.data.id)

    @pytest.mark.parametrize('existing_data, error', [
        ({'name': data.fake.name(), 'barcode': data.fake.ean13()}, {
            'name': ['customer with this name already exists.'],
            'barcode': ['customer with this barcode already exists.']
        }),
        ({'name': data.fake.name()}, {
            'name': ['customer with this name already exists.']
        }),
        ({'barcode': data.fake.ean13()}, {
            'barcode': ['customer with this barcode already exists.']
        }),
    ])
    @users(User.SUPERUSER)
    def test_createCustomerWithExistingNameAndBarcode_returns400AndError(self, client, user, existing_data, error):
        # Setup
        payload = data.fake.model.customer(**existing_data)
        response, model = CustomerAPI(client).create_customer(data=payload)
        customer_id = model.data.id

        # Act and assert
        payload = data.fake.model.customer(**existing_data)
        response, model = CustomerAPI(client).create_customer(data=payload)
        APIResponse(response).check_status(400)
        assert model.error == error

        # Cleanup
        CustomerAPI(client).delete_customer(id=customer_id)

    @users(User.SUPERUSER)
    def test_getAllCustomers_return200AndData(self, client, user):
        response, model = CustomerAPI(client).get_all_customers()
        APIResponse(response).check_status(200)

    @users(User.SUPERUSER)
    def test_getCustomerByID_returns200AndData(self, client, user):
        # Setup
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).create_customer(data=payload)
        customer_id = model.data.id

        # Act and assert
        response, model = CustomerAPI(client).get_customer(id=customer_id)
        APIResponse(response).check_status(200)

    @users(User.SUPERUSER)
    def test_updateCustomerByID_returns200AndData(self, client, user):
        # Setup
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).create_customer(data=payload)
        customer_id = model.data.id

        # Act and assert
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).update_customer(id=customer_id, data=payload)
        APIResponse(response).check_status(200)
        assert customer_id == model.data.id, 'Old ID and new ID are not matching.'
        assert payload['name'] == model.data.name
        assert payload['barcode'] == model.data.barcode

        # Clean up
        CustomerAPI(client).delete_customer(id=customer_id)

    @users(User.SUPERUSER)
    def test_updateCustomerByIDWithExistingNameAndBarcode_returns400AndError(self, client, user):
        # Setup
        payload = data.fake.model.customer()
        response, model_1 = CustomerAPI(client).create_customer(data=payload)
        payload = data.fake.model.customer()
        response, model_2 = CustomerAPI(client).create_customer(data=payload)

        # Act and assert
        payload = data.fake.model.customer(name=model_1.data.name, barcode=model_1.data.barcode)
        response, model = CustomerAPI(client).update_customer(id=model_2.data.id, data=payload)
        APIResponse(response).check_status(400)
        assert model.error == {
            'name': ['customer with this name already exists.'],
            'barcode': ['customer with this barcode already exists.']
        }

        # Clean up
        CustomerAPI(client).delete_customer(id=model_1.data.id)
        CustomerAPI(client).delete_customer(id=model_2.data.id)

    @users(User.SUPERUSER)
    def test_deleteCustomerByID_returns204(self, client, user):
        # Setup
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).create_customer(data=payload)

        # Act and assert
        response, model = CustomerAPI(client).delete_customer(id=model.data.id)
        APIResponse(response).check_status(204)

    @users(User.SUPERUSER)
    def test_deleteNotExistingCustomerByID_returns404AndError(self, client, user):
        # Act and assert
        not_existing_customer_id = data.fake.uuid4()
        response, model = CustomerAPI(client).delete_customer(id=not_existing_customer_id)
        APIResponse(response).check_status(404)
        assert model.error['detail'] == 'Not found.'

    @users(User.NONE)
    def test_unauthCRUDRequest_returns401AndError(self, client, user):
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).create_customer(data=payload)
        UnauthRequestErrorResponse(**response.json())

    @users(User.SUPERUSER)
    def test_authRequestWithoutSection_returns400AndError(self, client, user):
        response, model = CustomerAPI(client).send_request_without_section_param('GET', 1)
        APIResponse(response).check_status(400)
        assert model.error['message'] == 'There is no such menu route available.'

    @pytest.mark.skip(reason="Facility user should be created automatically")
    @users(User.FACILITY_USER)
    def test_userWithNoPermissionToView_returns403AndError(self, client, user):
        ...

    @pytest.mark.skip(reason="Facility user should be created automatically")
    @users(User.FACILITY_USER)
    def test_userWithNoPermissionToEdit_returns403AndError(self, client, user):
        ...
