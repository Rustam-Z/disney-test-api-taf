import data
from api.endpoints.items.inventory_category_api import InventoryCategoryAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateInventoryCategory:
    @users(User.SUPERUSER)
    def test_createInventoryCategoryBySuperuser_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_inventory_category')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)


class TestDeleteInventoryCategory:
    @users(User.SUPERUSER)
    def test_deleteInventoryCategoryBySuperuser_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_inventory_category')()
        id_ = model.data.id

        # Act
        response, model = InventoryCategoryAPI(client).delete_category(id=id_)

        # Assert
        APIResponse(response).assert_status(204)
