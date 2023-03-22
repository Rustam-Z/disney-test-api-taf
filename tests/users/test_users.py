"""
TODO: test pagination in get all users
"""
import pytest

from api.requests.users_api import UsersAPI
from core.api_response import APIResponse
from core.decorators import users
from core.enums.users import User
from tests.users.users_fixtures import create_fake_user, create_fake_user_without_facility


class TestUsersCRUD:
    @users(User.SUPERUSER)
    def test_superuserCreatesUser_returns201AndData(self, client, user, request):
        payload, response, model = request.getfixturevalue('create_fake_user')()
        APIResponse(response).check_status(201)

    @users(User.FACILITY_ADMIN)
    def test_adminCreatesUser_returns201AndData(self, client, user, request):
        payload, response, model = request.getfixturevalue('create_fake_user_without_facility')()
        APIResponse(response).check_status(201)

    @users(User.SUPERUSER)
    def test_superuserGetsAllUsers_return200AndData(self, client, user):
        response, model = UsersAPI(client).get_all_users()
        APIResponse(response).check_status(200)

    @users(User.FACILITY_ADMIN)
    def test_adminGetsAllUsers_return200AndData(self, client, user):
        response, model = UsersAPI(client).get_all_users()
        APIResponse(response).check_status(200)
        # TODO: verify that the users belong to the same facility

    @users(User.SUPERUSER)
    def test_superuserGetsUserByID_returns200AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_user')()
        existing_id = model.data.id

        # Act and assert
        response, model = UsersAPI(client).get_user(id=existing_id)
        APIResponse(response).check_status(200)
        assert model.data.id == existing_id, 'IDs are not matching.'

    @users(User.FACILITY_ADMIN)
    def test_adminGetsUserByID_returns200AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_user_without_facility')()
        existing_id = model.data.id

        # Act and assert
        response, model = UsersAPI(client).get_user(id=existing_id)
        APIResponse(response).check_status(200)
        assert model.data.id == existing_id, 'IDs are not matching.'

    @pytest.mark.skip(reason='TODO')
    @users(User.SUPERUSER)
    def test_updateUserByID_returns200AndData(self, client, user, request):
        # Create a user
        # Get a user
        # Change the response body
        # Verify that status is 200 and the data was altered
        ...

    @users(User.SUPERUSER)
    def test_deleteRoleByID_returns204(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_user')()
        existing_id = model.data.id

        # Act and assert
        response, model = UsersAPI(client).delete_user(id=existing_id)
        APIResponse(response).check_status(204)

        # Fetching removed item
        response, model = UsersAPI(client).get_user(id=existing_id)
        APIResponse(response).check_status(404)
        assert model.error['detail'] == 'Not found.'  # TODO: error message should not be validated here.


class TestUsersAuth:
    ...


class TestUsersWithoutSectionParam:
    ...

