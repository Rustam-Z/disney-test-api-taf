"""
Test facility CRUD.
"""
import pytest

import data
from api.requests.facility_api import FacilityAPI
from api.responses.common_models import AuthErrorResponse, RequestWithoutSectionParamErrorResponse
from core.api_response import APIResponse
from core.decorators import users
from core.enums.users import User


class TestFacilityCRUD:
    @users(User.SUPERUSER)
    def test_createNewFacility_returns201AndData(self, client, user, request):
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=1)
        APIResponse(response).check_status(201)

    @users(User.SUPERUSER)
    def test_createNewFacilityWithNoCustomers_returns201AndError(self, client, user, request):
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=0)
        APIResponse(response).check_status(201)

    @users(User.SUPERUSER)
    def test_createNewFacilityWithMultipleCustomers_returns201AndData(self, client, user, request):
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=2)
        APIResponse(response).check_status(201)

    @users(User.SUPERUSER)
    def test_createFacilityWithExistingName_returns400AndError(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_facility')()
        existing_facility_name = model.data.name

        # Act and assert
        payload = data.fake.model.facility(name=existing_facility_name)
        response, model = FacilityAPI(client).create_facility(data=payload)
        APIResponse(response).check_status(400)
        assert model.error['name'] == ['facility with this name already exists.']

    @users(User.SUPERUSER)
    def test_createFacilityWithWrongTurnaroundTime_returns400AndError(self, client, user, request):
        wrong_turnaround_time = 13
        payload = data.fake.model.facility(turnaround_time=wrong_turnaround_time)
        response, model = FacilityAPI(client).create_facility(data=payload)
        APIResponse(response).check_status(400)
        assert model.error['turnaround_time'] == ['"13" is not a valid choice.']

    @users(User.SUPERUSER)
    def test_getAllFacilities_return200AndData(self, client, user):
        response, model = FacilityAPI(client).get_all_facilities()
        APIResponse(response).check_status(200)

    @users(User.SUPERUSER)
    def test_getFacilityByID_returns200AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=1)
        existing_facility_id = model.data.id

        # Act and assert
        response, model = FacilityAPI(client).get_facility(id=existing_facility_id)
        APIResponse(response).check_status(200)
        assert model.data.id == existing_facility_id, 'IDs are not matching.'

    @users(User.SUPERUSER)
    def test_updateFacilityByID_returns200AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=1)
        existing_facility_id = model.data.id

        # Act and assert
        payload = data.fake.model.facility()
        response, model = FacilityAPI(client).update_facility(id=existing_facility_id,
                                                              data=payload)
        APIResponse(response).check_status(200)
        assert existing_facility_id == model.data.id, 'Old ID and new ID are not matching.'
        assert payload['name'] == model.data.name

    @pytest.mark.skip(reason="TODO")
    @users(User.SUPERUSER)
    def test_updateFacilityByIDWithExistingName_returns400AndError(self, client, user):
        ...

    @users(User.SUPERUSER)
    def test_deleteFacilityByID_returns204(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_facility')(no_of_customers=1)
        existing_facility_id = model.data.id

        # Act and assert
        response, model = FacilityAPI(client).delete_facility(id=existing_facility_id)
        APIResponse(response).check_status(204)

    @pytest.mark.skip(reason="TODO")
    @users(User.SUPERUSER)
    def test_deleteNotExistingFacilityByID_returns404AndError(self, client, user):
        ...


class TestFacilityAuth:
    @users(User.NONE)
    def test_unauthCRUDRequest_returns400AndError(self, client, user):
        payload = data.fake.model.facility()
        response, model = FacilityAPI(client).create_facility(data=payload)
        APIResponse(response).check_status(400)
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
    @pytest.mark.skip(reason='Get all facilities is allowed without section param.')
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_GET_ALL_returns400AndError(self, client, user):
        response, model = FacilityAPI(client).send_request_without_section_param('GET')
        APIResponse(response).check_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())

    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_POST_returns400AndError(self, client, user):
        response, model = FacilityAPI(client).send_request_without_section_param('POST')
        APIResponse(response).check_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())

    @pytest.mark.parametrize('method', ['GET', 'PATCH', 'DELETE'])
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_GET_PATCH_DELETE_returns400AndError(self, client, user, method):
        not_existing_id = data.fake.uuid4()
        response, model = FacilityAPI(client).send_request_without_section_param(method, id=not_existing_id)
        APIResponse(response).check_status(400)
        RequestWithoutSectionParamErrorResponse(**response.json())
