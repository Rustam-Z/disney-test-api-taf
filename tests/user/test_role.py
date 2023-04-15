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
from fixtures.role import create_fake_role


class TestRoleCRUD:
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_createNewRole_returns201AndData(self, client, user, request):
        payload, response, model = request.getfixturevalue('create_fake_role')()
        APIResponse(response).assert_status(201)

    @users(User.SUPERUSER)
    def test_getAllRoles_return200AndData(self, client, user):
        response, model = RoleAPI(client).get_all_roles()
        APIResponse(response).assert_status(200)

    @users(User.SUPERUSER)
    def test_getRoleByID_returns200AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_role')(is_driver=True)
        existing_role_id = model.data.id

        # Act and assert
        response, model = RoleAPI(client).get_role(id=existing_role_id)
        APIResponse(response).assert_status(200)
        assert model.data.id == existing_role_id, 'IDs are not matching.'

    @users(User.SUPERUSER)
    def test_updateRoleByID_returns200AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_role')()
        existing_role_id = model.data.id

        # Act and assert
        menu_list_response, menu_list_model = MenuAPI(client).get_menu_list()
        payload = data.fake.model.role(sections=menu_list_model.data.results)
        response, model = RoleAPI(client).update_role(id=existing_role_id,
                                                      data=payload)
        APIResponse(response).assert_status(200)
        assert existing_role_id == model.data.id, 'Old ID and new ID are not matching.'
        assert payload.get('name') == model.data.name

    @users(User.SUPERUSER)
    def test_deleteRoleByID_returns204(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_role')()
        existing_role_id = model.data.id

        # Act and assert
        response, model = RoleAPI(client).delete_role(id=existing_role_id)
        APIResponse(response).assert_status(204)

    @users(User.SUPERUSER)
    def test_deleteFacility_byInvalidID_returns404AndError(self, client, user):
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
