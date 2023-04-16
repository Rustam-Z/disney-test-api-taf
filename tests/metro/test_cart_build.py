from api.endpoints.metro.metro_api import MetroAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
from fixtures.cart_build import create_fake_cart_superuser


class TestCreateCart:
    @users(User.SUPERUSER)
    def test_createCart_withValidData_returns201AndData(self, client, user, request):
        payload, response, model = request.getfixturevalue('create_fake_cart_superuser')()
        pass
