"""
Test customer CRUD.
"""
import pytest

from api.requests.customer_api import CustomerAPI
from core.api_response import APIResponse
from core.decorators import users
from core.enums.users import User
import data


class TestCustomer:
    @users(User.SUPERUSER)
    def test_createNewCustomer_returns201AndData(self, client, user):
        # TODO: create pydantic model for request payload
        payload = {
            'name': data.fake.name(),
            'barcode': data.fake.ean13(),
            'address_line1': data.fake.address(),
            'address_line2': data.fake.address(),
            'city': data.fake.city(),
            'state': data.fake.state(),
            'country': data.fake.country(),
            'zip_code': data.fake.zipcode(),
            'main_phone_number': data.fake.custom_phone_number(),
        }
        response, model = CustomerAPI(client).create_customer(data=payload)
        APIResponse(response).check_status(201)
        # TODO: Create teardown

    @users(User.SUPERUSER)
    def test_createCustomerWithExistingNameAndBarcode_returns400AndError(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_createCustomerWithExistingName_returns400AndError(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_createCustomerWithExistingBarcode_returns400AndError(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_getAllCustomers_return200AndData(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_getCustomerByID_returns200AndData(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_updateCustomerByID_returns200AndData(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_updateCustomerByIDWithExistingNameAndBarcode_returns400AndError(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_deleteCustomerByID_returns204(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_deleteNotExistingCustomerByID_returns404AndError(self, client, user):
        ...

    @users(User.NONE)
    def test_unauthCRUDRequest_returns401AndError(self, client, user):
        ...

    @pytest.mark.skip(reason="Facility user should be created automatically")
    @users(User.FACILITY_USER)
    def test_userWithNoPermissionToView_returns403AndError(self, client, user):
        ...

    @pytest.mark.skip(reason="Facility user should be created automatically")
    @users(User.FACILITY_USER)
    def test_userWithNoPermissionToEdit_returns403AndError(self, client, user):
        ...
