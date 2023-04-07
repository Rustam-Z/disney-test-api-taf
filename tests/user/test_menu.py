"""
Tests for fetching all menu items, and user menu items based on user permissions.
"""

from api.requests.menu_api import MenuAPI
from api.responses.common_models import AuthErrorResponse
from core.asserters import APIResponse
from core.enums.users import User
from core.decorators import users, mobile


class TestMenu:
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_getMenuList_returnsAllMenuListItems(self, client, user):
        response, model = MenuAPI(client).get_menu_list()
        APIResponse(response).assert_status(200)
        assert len(model.data.results) == 21, '21 menu items should be there, some menus were deleted or added.'

    @mobile()
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_getUserMenus_returnsCorrectUserMenus(self, client, user, is_for_mobile):
        """
        TODO: To verify that correct edit, view permissions are fetched,
        we need to create a role, assign it to user.
        """
        response, model = MenuAPI(client).get_user_menus(is_for_mobile=is_for_mobile)
        APIResponse(response).assert_status(200)

    @users(User.NONE)
    def test_unauthGetMenuList_returnsError(self, client, user):
        response, model = MenuAPI(client).get_menu_list()
        APIResponse(response).assert_status(401)
        AuthErrorResponse(**response.json())

    @mobile()
    @users(User.NONE)
    def test_unauthGetUserMenus_returnsError(self, client, user, is_for_mobile):
        response, model = MenuAPI(client).get_user_menus(is_for_mobile=is_for_mobile)
        APIResponse(response).assert_status(401)
        AuthErrorResponse(**response.json())
