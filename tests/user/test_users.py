"""
TODO: test pagination in get all users
"""
import pytest

import data
from api.endpoints.user.users_api import UsersAPI
from api.enums.errors import ErrorDetail
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateUser:
    @users(User.SUPERUSER)
    def test_createUserBySuperuser_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_user_superuser')()

        # Assert
        APIResponse(response).assert_status(201)

    @users(User.FACILITY_ADMIN)
    def test_createUserByFacilityAdmin_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_user')()

        # Assert
        APIResponse(response).assert_status(201)


class TestGetAllUsers:
    @users(User.SUPERUSER)
    def test_getAllUsersByFacilityAdmin_returns200AndData(self, client, user):
        # Act
        response, model = UsersAPI(client).get_all_users()

        # Assert
        APIResponse(response).assert_status(200)

    @users(User.FACILITY_ADMIN)
    def test_getAllUsersByFacilityAdmin_returns200AndData(self, client, user):
        # Act
        response, model = UsersAPI(client).get_all_users()

        # Assert
        APIResponse(response).assert_status(200)
        # TODO: verify that the users belong to the same facility


class TestGetUser:
    @users(User.SUPERUSER)
    def test_getsUserBySuperuser_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_user_superuser')()
        existing_id = model.data.id

        # Act
        response, model = UsersAPI(client).get_user(id=existing_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == existing_id, 'IDs are not matching.'

    @users(User.FACILITY_ADMIN)
    def test_getsUserByFacilityAdmin_withValidID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_user')()
        existing_id = model.data.id

        # Act
        response, model = UsersAPI(client).get_user(id=existing_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == existing_id, 'IDs are not matching.'


class TestUpdateUser:
    @users(User.SUPERUSER)
    def test_updateUserBySuperUser_withValidData_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_user_superuser')()
        existing_id = model.data.id
        request_payload = data.fake.model.user()

        # Act
        response, model = UsersAPI(client).update_user(id=existing_id, data=request_payload)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == existing_id, 'IDs are not matching.'


class TestDeleteUser:
    @users(User.SUPERUSER)
    def test_deleteRoleBySuperuser_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_user_superuser')()
        existing_id = model.data.id

        # Act
        response, _ = UsersAPI(client).delete_user(id=existing_id)

        # Assert
        APIResponse(response).assert_status(204)

        # Act: Fetching removed item.
        response, model = UsersAPI(client).get_user(id=existing_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == ErrorDetail.NOT_FOUND.value


class TestUsersAuth:
    ...


class TestUsersWithoutSectionParam:
    ...
