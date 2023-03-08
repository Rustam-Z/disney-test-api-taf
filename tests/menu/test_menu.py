"""
Test fetching all menu items, and user menu items
based on user permissions.
"""


class TestMenu:
    def test_authRequest_returnsAllMenuListItems(self, client):
        """
        TODO: @auth(<USER_TYPE>) should be created to authenticate the request.
        """
        ...

    def test_authRequest_returnsCorrectUserMenus(self, client):
        """
        To verify that correct edit, view permissions are fetched,
        we need to create a role, assign it to user.
        """
        ...

    def test_unauthRequest_returnsError(self, client):
        """
        Test user-menus with @mobile
        TODO: @mobile() should be created to create two requests
        """
        ...
