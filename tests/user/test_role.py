"""
TODO: test pagination in get all roles
TODO: create a role with facility id
TODO: create a role, and a user, assign role to that user, remove the role, what will happen with this user?
"""

import data
from api.endpoints.user.menu_api import MenuAPI
from api.endpoints.user.role_api import RoleAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateRole:
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_createRoleBySuperuser_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_role')()
        
        # Assert
        APIResponse(response).assert_status(201)


class TestGetAllRoles:
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_getAllRoles_return200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_role')()

        # Act
        response, model = RoleAPI(client).get_all_roles()
        
        # Assert
        APIResponse(response).assert_status(200)


class TestGetRole:
    @users(User.SUPERUSER)
    def test_getRoleBySuperuser_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_role')(is_driver=True)
        existing_role_id = model.data.id

        # Act
        response, model = RoleAPI(client).get_role(id=existing_role_id)

        # Assert
        APIResponse(response).assert_status(200)
        assert model.data.id == existing_role_id, 'IDs are not matching.'


class TestUpdateRole:
    @users(User.SUPERUSER)
    def test_updateRoleByID_returns200AndData(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_role')()
        menu_list_response, menu_list_model = MenuAPI(client).get_menu_list()
        existing_role_id = model.data.id

        # Act
        payload = data.fake.model.role(sections=menu_list_model.data.results)
        response, model = RoleAPI(client).update_role(id=existing_role_id, data=payload)

        # Assert4
        APIResponse(response).assert_status(200)
        assert existing_role_id == model.data.id, 'Old ID and new ID are not matching.'
        assert payload.get('name') == model.data.name


class TestDeleteRole:
    @users(User.SUPERUSER)
    def test_deleteRoleBySuperuser_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_role')()
        existing_role_id = model.data.id

        # Act
        response, model = RoleAPI(client).delete_role(id=existing_role_id)

        # Assert
        APIResponse(response).assert_status(204)

    @users(User.SUPERUSER)
    def test_deleteRoleBySuperuser_withInvalidID_returns404AndError(self, client, user):
        # Arrange
        not_existing_id = data.fake.uuid4()

        # Act
        response, model = RoleAPI(client).delete_role(id=not_existing_id)

        # Assert
        APIResponse(response).assert_status(404)
        assert model.error.get('detail') == 'Not found.'


class TestRoleAuth:
    ...


class TestRoleWithoutSectionParam:
    ...
