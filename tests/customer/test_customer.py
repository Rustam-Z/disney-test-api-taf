"""
Test customer CRUD.

TODO: test pagination in get all customers, test creating without mandatory fields.
TODO: add test to check status update.
"""
import pytest

from api.requests.customer_api import CustomerAPI
from api.responses.common_models import AuthErrorResponse, RequestWithoutSectionParamErrorResponse
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
import data
from tests.fixtures.customer_fixtures import create_fake_customer


class TestCustomerCRUD:

    @users(User.SUPERUSER)
    def test_createNewCustomer_returns201AndData(self, client, user, request):
        # Act and assert
        payload, response, model = request.getfixturevalue('create_fake_customer')()
        APIResponse(response).assert_status(201)
        assert payload.get('name') == model.data.name
        assert payload.get('barcode') == model.data.barcode

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
    def test_createCustomerWithExistingNameAndBarcode_returns400AndError(
            self,
            client,
            user,
            existing_data,
            error,
            request
    ):
        # Setup
        request.getfixturevalue('create_fake_customer')(**existing_data)

        # Act and assert
        payload = data.fake.model.customer(**existing_data)
        response, model = CustomerAPI(client).create_customer(data=payload)
        APIResponse(response).assert_status(400)
        assert model.error == error

    @users(User.SUPERUSER)
    def test_getAllCustomers_return200AndData(self, client, user):
        response, model = CustomerAPI(client).get_all_customers()
        APIResponse(response).assert_status(200)

    @users(User.SUPERUSER)
    def test_getCustomerByID_returns200AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_customer')()
        customer_id = model.data.id

        # Act and assert
        response, model = CustomerAPI(client).get_customer(id=customer_id)
        APIResponse(response).assert_status(200)

    @users(User.SUPERUSER)
    def test_updateCustomerByID_returns200AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_customer')()
        customer_id = model.data.id

        # Act and assert
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).update_customer(id=customer_id, data=payload)
        APIResponse(response).assert_status(200)
        assert customer_id == model.data.id, 'Old ID and new ID are not matching.'
        assert payload.get('name') == model.data.name
        assert payload.get('barcode') == model.data.barcode

    @users(User.SUPERUSER)
    def test_updateCustomerByIDWithExistingNameAndBarcode_returns400AndError(self, client, user, request):
        # Setup
        payload, response, model_1 = request.getfixturevalue('create_fake_customer')()
        payload, response, model_2 = request.getfixturevalue('create_fake_customer')()

        # Act and assert
        payload = data.fake.model.customer(name=model_1.data.name, barcode=model_1.data.barcode)
        response, model = CustomerAPI(client).update_customer(id=model_2.data.id, data=payload)
        APIResponse(response).assert_status(400)
        assert model.error == {
            'name': ['customer with this name already exists.'],
            'barcode': ['customer with this barcode already exists.']
        }

    @users(User.SUPERUSER)
    def test_deleteCustomerByID_returns204(self, client, user):
        # Setup
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).create_customer(data=payload)

        # Act and assert
        response, model = CustomerAPI(client).delete_customer(id=model.data.id)
        APIResponse(response).assert_status(204)

    @users(User.SUPERUSER)
    def test_deleteNotExistingCustomerByID_returns404AndError(self, client, user):
        # Act and assert
        not_existing_customer_id = data.fake.uuid4()
        response, model = CustomerAPI(client).delete_customer(id=not_existing_customer_id)
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == 'Not found.'


class TestCustomerAuth:
    @users(User.NONE)
    def test_unauthCRUDRequest_returns400AndError(self, client, user):
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).create_customer(data=payload)
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @pytest.mark.skip(reason="Facility user should be created automatically")
    @users(User.FACILITY_USER)
    def test_userWithNoPermissionToView_returns403AndError(self, client, user):
        ...

    @pytest.mark.skip(reason="Facility user should be created automatically")
    @users(User.FACILITY_USER)
    def test_userWithNoPermissionToEdit_returns403AndError(self, client, user):
        ...


class TestCustomerWithoutSectionParam:
    """
    For testing requests without section query param we don't need:
        - Request body for POST and PATCH.
        - ID for GET, DELETE, PATCH.

    Because existence of section param in URL is validated first.
    """

    @pytest.mark.skip(reason='Get all customers is allowed without section param.')
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_GET_ALL_returns400AndError(self, client, user):
        response, model = CustomerAPI(client).send_request_without_section_param('GET')
        APIResponse(response).assert_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())

    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_POST_returns400AndError(self, client, user):
        response, model = CustomerAPI(client).send_request_without_section_param('POST')
        APIResponse(response).assert_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())

    @pytest.mark.parametrize('method', ['GET', 'PATCH', 'DELETE'])
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_GET_PATCH_DELETE_returns400AndError(self, client, user, method):
        not_existing_id = data.fake.uuid4()
        response, model = CustomerAPI(client).send_request_without_section_param(method, id=not_existing_id)
        APIResponse(response).assert_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())
