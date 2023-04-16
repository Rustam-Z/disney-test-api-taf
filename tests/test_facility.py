import pytest

import data
from api.endpoints.facility_api import FacilityAPI
from api.response_models.common_models import (
    AuthErrorResponse,
    RequestWithoutSectionParamErrorResponse,
    OnlySuperuserCanPerformErrorResponse,
)
from api.response_models.facility_models import GetAllFacilitiesSuccessResponse
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestFacilityCRUD:
    @users(User.SUPERUSER)
    def test_createFacility_withValidData_returns201AndData(self, client, user):
        # Arrange
        payload = data.fake.model.facility()

        # Act
        response, model = FacilityAPI(client).create_facility(data=payload)

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

        # Cleanup
        try:
            FacilityAPI(client).delete_facility(id=model.id)
        except Exception:
            return None

    @users(User.SUPERUSER)
    def test_createFacility_withCustomer_returns201AndError(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=1)

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

    @users(User.SUPERUSER)
    def test_createFacility_withMultipleCustomers_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=2)

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

    @users(User.SUPERUSER)
    def test_createFacility_withExistingName_returns400AndError(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_facility')()
        existing_facility_name = model.data.name

        # Act
        payload = data.fake.model.facility(name=existing_facility_name)
        response, model = FacilityAPI(client).create_facility(data=payload)

        # Assert
        APIResponse(response).assert_status(400)
        assert model.error.get('name') == ['facility with this name already exists.']

    @users(User.SUPERUSER)
    def test_getAllFacilities_returns200AndData(self, client, user):
        response, model = FacilityAPI(client).get_all_facilities()
        APIResponse(response).assert_status(200)

    @users(User.SUPERUSER)
    def test_getFacility_byValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_facility')()
        existing_facility_id = model.data.id

        # Act
        response, model = FacilityAPI(client).get_facility(id=existing_facility_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == existing_facility_id, 'IDs are not matching.'

    @users(User.SUPERUSER)
    def test_updateFacility_byValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_facility')()
        existing_facility_id = model.data.id

        # Act
        payload = data.fake.model.facility()
        response, model = FacilityAPI(client).update_facility(id=existing_facility_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        APIResponse(response).assert_models(payload)
        assert existing_facility_id == model.data.id, 'Old ID and new ID are not matching.'

    @users(User.SUPERUSER)
    def test_updateFacilityStatus_byValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_facility')()
        existing_facility_id = model.data.id

        # Act
        payload = {'status': 'inactive'}
        response, model = FacilityAPI(client).update_facility(id=existing_facility_id, data=payload)

        # Assert
        APIResponse(response).assert_status(200)
        assert existing_facility_id == model.data.id, 'Old ID and new ID are not matching.'
        assert payload.get('status') == model.data.status

    @pytest.mark.skip(reason="TODO")
    @users(User.SUPERUSER)
    def test_updateFacility_byValidIDWithExistingName_returns400AndError(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_deleteFacility_byValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_facility')()
        existing_facility_id = model.data.id

        # Act
        response, model = FacilityAPI(client).delete_facility(id=existing_facility_id)

        # Assert
        APIResponse(response).assert_status(204)

    @users(User.SUPERUSER)
    def test_deleteFacility_byInvalidID_returns404AndError(self, client, user):
        # Arrange
        not_existing_id = data.fake.uuid4()

        # Act
        response, model = FacilityAPI(client).delete_facility(id=not_existing_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == 'Not found.'


class TestFacilityAuth:
    @users(User.FACILITY_ADMIN)
    def test_createFacility_notSuperUser_returns400AndOnlySuperuserError(self, client, user):
        # Act
        response, model = FacilityAPI(client).create_facility(data={})

        # Assert
        APIResponse(response).assert_status(400)
        OnlySuperuserCanPerformErrorResponse(**response.json())

    @users(User.NONE)
    def test_createCustomer_unauthRequest_returns400AndError(self, client, user):
        # Act
        response, model = FacilityAPI(client).create_facility(data={})

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_getCustomer_unauthRequest_returns400AndError(self, client, user):
        # Act
        response, model = FacilityAPI(client).get_facility(id=0)

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_getCustomers_unauthRequest_returns400AndError(self, client, user):
        # Act
        response, model = FacilityAPI(client).get_all_facilities()

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @users(User.NONE)
    def test_updateCustomer_unauthRequest_returns400AndError(self, client, user):
        # Act
        response, model = FacilityAPI(client).update_facility(id=0, data={})

        # Assert
        APIResponse(response).assert_status(400)
        AuthErrorResponse(**response.json())

    @pytest.mark.skip(reason="User should be created with no view permission automatically")
    @users(User.FACILITY_USER)
    def test_userWithNoPermissionToView_returns403AndError(self, client, user):
        ...

    @pytest.mark.skip(reason="User should be created with no edit permission automatically")
    @users(User.FACILITY_USER)
    def test_userWithNoPermissionToEdit_returns403AndError(self, client, user):
        ...


class TestFacilityWithoutSectionParam:
    _PATH = FacilityAPI.FACILITY

    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_GET_ALL_returns200AndData(self, client, user):
        """
        Get all customers is allowed without section param.
        """
        response = client.send_request('GET', path=self._PATH)
        APIResponse(response).assert_status(200)
        GetAllFacilitiesSuccessResponse(**response.json())

    @users(User.SUPERUSER)
    def test_POST_withSuperuser_returns400AndError(self, client, user):
        response = client.send_request('POST', path=self._PATH)
        APIResponse(response).assert_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())

    @users(User.FACILITY_ADMIN)
    def test_POST_returns400AndError(self, client, user):
        response = client.send_request('POST', path=self._PATH)
        APIResponse(response).assert_status(400)
        OnlySuperuserCanPerformErrorResponse(**response.json())

    @users(User.SUPERUSER, User.FACILITY_USER)
    def test_GET_returns400AndError(self, client, user):
        path = f'{self._PATH}{data.fake.uuid4()}'
        response = client.send_request('GET', path)
        APIResponse(response).assert_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())

    @pytest.mark.parametrize('method', ['PATCH', 'DELETE'])
    @users(User.SUPERUSER)
    def test_PATCH_DELETE_withSuperuser_returns400AndError(self, client, user, method):
        path = f'{self._PATH}{data.fake.uuid4()}'
        response = client.send_request(method, path)
        APIResponse(response).assert_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())

    @pytest.mark.parametrize('method', ['PATCH', 'DELETE'])
    @users(User.FACILITY_USER)
    def test_PATCH_DELETE_returns400AndError(self, client, user, method):
        path = f'{self._PATH}{data.fake.uuid4()}'
        response = client.send_request(method, path)
        APIResponse(response).assert_status(400)
        OnlySuperuserCanPerformErrorResponse(**response.json())
