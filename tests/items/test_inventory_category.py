"""
TODO:
- Test CRUD
- Auth
- Section
"""
import data
from api.endpoints.items.inventory_category_api import InventoryCategoryAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
from fixtures.inventory_item_type import create_fake_inventory_item_type


class TestInventoryCategoryCRUD:
    @users(User.SUPERUSER)
    def test_superUserCreatesCategory_returns201AndData(self, client, user):
        # Arrange
        payload = data.fake.model.inventory_category()

        # Act
        response, model = InventoryCategoryAPI(client).create_category(data=payload)
        id_ = model.data.id

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)

        # Cleanup
        try:
            InventoryCategoryAPI(client).delete_category(id=id_, expect_json=False)
        except Exception:
            return None

    @users(User.SUPERUSER)
    def test_superUserDeletesCategory_returns204(self, client, user):
        # Arrange
        payload = data.fake.model.inventory_category()
        response, model = InventoryCategoryAPI(client).create_category(data=payload)
        id_ = model.data.id

        # Act
        response, model = InventoryCategoryAPI(client).delete_category(id=id_)

        # Assert
        APIResponse(response).assert_status(204)
