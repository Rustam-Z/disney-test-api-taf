"""
Test fetching all menu items, and user menu items based on user permissions.
"""
from core.enums.users import User
from core.decorators import users


class TestMenu:
    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_authRequest_returnsAllMenuListItems(self, client, user):
        pass

    @users(User.SUPERUSER, User.FACILITY_ADMIN)
    def test_authRequest_returnsCorrectUserMenus(self, client, user):
        """
        To verify that correct edit, view permissions are fetched,
        we need to create a role, assign it to user.
        """
        pass

    @users(User.NONE)
    def test_unauthRequest_returnsError(self, client, user):
        """
        Test user-menus with @mobile
        TODO: @mobile() should be created to create two requests
        """
        pass
