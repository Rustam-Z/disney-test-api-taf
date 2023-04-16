"""
TODO:
- Test CRUD
    - Create with existing name
    - Create with not existing category id
    - Create without description, expected: item should be created
- Auth
- Section
"""

from api.endpoints.items.inventory_item_type_api import InventoryItemTypeAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestCreateInventoryItemType:
    @users(User.SUPERUSER)
    def test_createInventoryItemTypeBySuperuser_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_inventory_item_type')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)


class TestDeleteInventoryItemType:
    @users(User.SUPERUSER)
    def test_deleteInventoryItemTypeBySuperuser_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_inventory_item_type')()
        existing_id = model.data.id

        # Act
        response, model = InventoryItemTypeAPI(client).delete_item_type(id=existing_id)

        # Assert
        APIResponse(response).assert_status(204)
