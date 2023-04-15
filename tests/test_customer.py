"""
TODO:
    - test pagination in get all customers, test creating without mandatory fields.
    - add test to check status update.
"""
import pytest

from api.endpoints.customer_api import CustomerAPI
from api.response_models.common_models import (
    AuthErrorResponse,
    RequestWithoutSectionParamErrorResponse,
    NoPermissionErrorResponse,
)
from api.response_models.customer_models import GetAllCustomersSuccessResponse
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
import data
from fixtures.customer import create_fake_customer


class TestCustomerCRUD:
    """
    Test customer CRUD (creation, reading, update, delete).
    """

    @users(User.SUPERUSER)
    def test_createCustomer_withValidData_returns201AndData(self, client, user, request):
        # Arrange
        payload = data.fake.model.customer()

        # Act
        response, model = CustomerAPI(client).create_customer(data=payload)

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

        # Cleanup
        try:
            CustomerAPI(client).delete_customer(id=model.id)
        except Exception:
            return None

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
    def test_createCustomer_withExistingNameAndBarcode_returns400AndError(
        self, client, user, request,
        existing_data, error,
    ):
        # Arrange
        request.getfixturevalue('create_fake_customer')(**existing_data)

        # Act
        payload = data.fake.model.customer(**existing_data)
        response, model = CustomerAPI(client).create_customer(data=payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error == error

    @users(User.SUPERUSER)
    def test_getAllCustomers_returns200AndData(self, client, user):
        response, model = CustomerAPI(client).get_all_customers()
        APIResponse(response).assert_status(200)

    @users(User.SUPERUSER)
    def test_getCustomer_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_customer')()
        customer_id = model.data.id

        # Act
        response, model = CustomerAPI(client).get_customer(id=customer_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == customer_id, 'IDs are not matching.'

    @users(User.SUPERUSER)
    def test_updateCustomer_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_customer')()
        customer_id = model.data.id

        # Act
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).update_customer(id=customer_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        APIResponse(response).assert_models(payload)
        assert customer_id == model.data.id, 'Old ID and new ID are not matching. Data was changed for wrong ID.'

    @users(User.SUPERUSER)
    def test_updateCustomer_withExistingNameAndBarcode_returns400AndError(self, client, user, request):
        # Arrange
        payload, response, model_1 = request.getfixturevalue('create_fake_customer')()
        payload, response, model_2 = request.getfixturevalue('create_fake_customer')()

        # Act
        payload = data.fake.model.customer(name=model_1.data.name, barcode=model_1.data.barcode)
        response, model = CustomerAPI(client).update_customer(id=model_2.data.id, data=payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error == {
            'name': ['customer with this name already exists.'],
            'barcode': ['customer with this barcode already exists.']
        }

    @users(User.SUPERUSER)
    def test_deleteCustomer_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_customer')()

        # Act
        response, model = CustomerAPI(client).delete_customer(id=model.data.id)

        # Assert
        APIResponse(response).assert_status(204)

    @users(User.SUPERUSER)
    def test_deleteCustomer_withInvalidID_returns404AndError(self, client, user):
        # Arrange
        not_existing_id = data.fake.uuid4()

        # Act
        response, model = CustomerAPI(client).delete_customer(id=not_existing_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == 'Not found.'


class TestCustomerAuth:
    """
    Test authentication and authorization.
    """

    @users(User.FACILITY_ADMIN)
    def test_createCustomer_notSuperUser_returns403AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).create_customer(data={})

        # Assert
        APIResponse(response).assert_status(403)
        NoPermissionErrorResponse(**response.json())

    @users(User.NONE)
    def test_createCustomer_unauthRequest_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).create_customer(data={})

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_getCustomer_unauthRequest_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).get_customer(id=0)

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_getCustomers_unauthRequest_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).get_all_customers()

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_updateCustomer_unauthRequest_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).update_customer(id=0, data={})

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @pytest.mark.skip(reason="Facility user should be created automatically")
    @users(User.FACILITY_USER)
    def test_request_withNoViewPermissionUser_returns403AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).get_customer(id=0)

        # Assert
        APIResponse(response).assert_status(403)

    @pytest.mark.skip(reason="Facility user should be created automatically")
    @users(User.FACILITY_USER)
    def test_request_withNoEditPermissionUser_returns403AndError(self, client, user):
        # Arrange
        payload = data.fake.model.customer()

        # Act
        response, model = CustomerAPI(client).create_customer(data=payload)

        # Assert
        APIResponse(response).assert_status(403)


class TestCustomerWithoutSectionParam:
    """
    For testing endpoints without section query param we don't need:
        - Request body_str for POST and PATCH.
        - ID for GET, DELETE, PATCH.

    Because existence of section param in URL is validated first.
    """
    _PATH = CustomerAPI.CUSTOMER

    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_GET_ALL_returns200AndData(self, client, user):
        """
        Get all customers is allowed without section param.
        """
        response = client.send_request('GET', path=self._PATH)
        APIResponse(response).assert_status(200)
        GetAllCustomersSuccessResponse(**response.json())

    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_POST_returns400AndError(self, client, user):
        response = client.send_request('POST', path=self._PATH)
        APIResponse(response).assert_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())

    @pytest.mark.parametrize('method', ['GET', 'PATCH', 'DELETE'])
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_GET_PATCH_DELETE_returns400AndError(self, client, user, method):
        path = f'{self._PATH}{data.fake.uuid4()}'
        response = client.send_request(method, path)
        APIResponse(response).assert_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())
