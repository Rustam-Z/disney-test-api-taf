"""
Test fetching all menu items, and user menu items based on user permissions.
"""
import pytest

from api.requests.menu_api import MenuAPI
from api.responses.common_models import AuthErrorResponse
from core.api_response import APIResponse
from core.enums.users import User
from core.decorators import users, mobile


class TestMenu:
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_authRequest_returnsAllMenuListItems(self, client, user):
        response, model = MenuAPI(client).get_menu_list()
        APIResponse(response).check_status(200)

    @mobile()
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_authRequest_returnsCorrectUserMenus(self, client, user, is_for_mobile):
        """
        TODO: To verify that correct edit, view permissions are fetched,
        we need to create a role, assign it to user.
        """
        response, model = MenuAPI(client).get_user_menus(is_for_mobile=is_for_mobile)
        APIResponse(response).check_status(200)

    @users(User.NONE)
    def test_unauthMenuListRequest_returnsError(self, client, user):
        response, model = MenuAPI(client).get_menu_list()

        APIResponse(response).check_status(401)
        assert model.error['detail'] == "Authentication credentials were not provided."
        # AuthErrorResponse(**response.json())

    @mobile()
    @users(User.NONE)
    def test_unauthUserMenusRequest_returnsError(self, client, user, is_for_mobile):
        response, model = MenuAPI(client).get_user_menus(is_for_mobile=is_for_mobile)

        APIResponse(response).check_status(401)
        assert model.error['detail'] == "Authentication credentials were not provided."
        # AuthErrorResponse(**response.json())
