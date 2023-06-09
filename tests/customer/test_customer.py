"""
TODO:
    - test pagination in get all customers
"""
import pytest

import data
from api.endpoints.customer.customer_api import CustomerAPI
from api.enums.errors import ErrorDetail
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
from api.response_models.customer.customer_models import GetAllCustomersSuccessResponse
from api.response_models.common_models import (
    AuthErrorResponse,
    RequestWithoutSectionParamErrorResponse,
    NoPermissionErrorResponse,
)


class TestCreateCustomer:
    @users(User.SUPERUSER)
    def test_createCustomer_withValidData_returns201AndData(self, client, user):
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

    @pytest.mark.parametrize('request_payload', [
        data.fake.model.customer(main_phone_number=data.fake.pystr()),  # Wrong data
        data.fake.model.customer().pop('name'),  # Removing mandatory param
    ])
    @users(User.SUPERUSER)
    def test_createCustomer_withWrongData_returns400AndError(self, client, user, request_payload):
        # Act
        response, model = CustomerAPI(client).create_customer(data=request_payload)

        # Assert
        APIResponse(response).assert_status(400)

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
        self, client, user, request, existing_data, error,
    ):
        # Arrange
        request.getfixturevalue('create_fake_customer')(**existing_data)

        # Act
        payload = data.fake.model.customer(**existing_data)
        response, model = CustomerAPI(client).create_customer(data=payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error == error

    @users(User.FACILITY_USER, User.FACILITY_ADMIN)
    def test_createCustomer_notSuperuser_returns403AndError(self, client, user):
        # Act
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).create_customer(data=payload)

        # Assert
        APIResponse(response).assert_status(403)
        NoPermissionErrorResponse(**response.json())


class TestGetAllCustomers:
    @users(User.SUPERUSER)
    def test_getAllCustomers_returns200AndData(self, client, user, request):
        # Arrange
        request.getfixturevalue('create_fake_customer')()

        # Act
        response, model = CustomerAPI(client).get_all_customers()

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.count > 0
        assert len(model.data.results) > 0


class TestGetCustomer:
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
    def test_getCustomer_withWrongID_returns404AndError(self, client, user):
        # Arrange
        customer_id = data.fake.ean()

        # Act
        response, model = CustomerAPI(client).get_customer(id=customer_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == 'Not found.'


class TestUpdateCustomer:
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
        assert customer_id == model.data.id, 'Old ID and new ID are not matching after UPDATE.'

    @users(User.SUPERUSER)
    def test_updateCustomer_updateStatusToInactive_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_customer')()
        customer_id = model.data.id

        # Act
        payload = {'status': 'inactive'}
        response, model = CustomerAPI(client).update_customer(id=customer_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == customer_id, 'Old ID and new ID are not matching after UPDATE.'
        assert model.data.status == payload.get('status')

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
    def test_updateCustomer_withWrongID_returns404AndError(self, client, user):
        # Arrange
        customer_id = data.fake.uuid4()

        # Act
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).update_customer(id=customer_id, data=payload)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == 'Not found.'

    @users(User.FACILITY_USER, User.FACILITY_ADMIN)
    def test_updateCustomer_notSuperuser_returns403AndError(self, client, user):
        # Arrange
        customer_id = data.fake.ean()

        # Act
        payload = data.fake.model.customer()
        response, model = CustomerAPI(client).update_customer(id=customer_id, data=payload)

        # Assert
        APIResponse(response).assert_status(403)
        NoPermissionErrorResponse(**response.json())


class TestDeleteCustomer:
    @users(User.SUPERUSER)
    def test_deleteCustomer_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_customer')()

        # Act
        response, model = CustomerAPI(client).delete_customer(id=model.data.id)

        # Assert
        APIResponse(response).assert_status(204)

    @users(User.SUPERUSER)
    def test_deleteCustomer_withWrongID_returns404AndError(self, client, user):
        # Arrange
        not_existing_id = data.fake.uuid4()

        # Act
        response, model = CustomerAPI(client).delete_customer(id=not_existing_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == ErrorDetail.NOT_FOUND.value


class TestCustomerAuth:
    """
    Test authentication.
    """

    @users(User.NONE)
    def test_createCustomer_withoutAuthorization_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).create_customer(data={})

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_getCustomer_withoutAuthorization_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).get_customer(id=0)

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_getCustomers_withoutAuthorization_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).get_all_customers()

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_updateCustomer_withoutAuthorization_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).update_customer(id=0, data={})

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_deleteCustomer_withoutAuthorization_returns400AndError(self, client, user):
        # Act
        response, model = CustomerAPI(client).delete_customer(id=0)

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())


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
