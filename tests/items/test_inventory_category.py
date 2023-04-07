"""
TODO:
- Test CRUD
- Auth
- Section
"""
import data
from api.requests.inventory_category_api import InventoryCategoryAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User


class TestInventoryCategoryCRUD:
    @users(User.SUPERUSER)
    def test_superUserCreatesCategory_returns201AndData(self, client, user):
        # Setup
        payload = data.fake.model.inventory_category()

        # Act and assert
        response, model = InventoryCategoryAPI(client).create_category(data=payload)
        id_ = model.data.id
        APIResponse(response).assert_status(201)
        assert model.data.name == payload.get('name')

        # Cleanup
        InventoryCategoryAPI(client).delete_category(id=id_)

    @users(User.SUPERUSER)
    def test_superUserDeletesCategory_returns204(self, client, user):
        # Setup
        payload = data.fake.model.inventory_category()
        response, model = InventoryCategoryAPI(client).create_category(data=payload)
        id_ = model.data.id

        # Act and assert
        response, _ = InventoryCategoryAPI(client).delete_category(id=id_)
        APIResponse(response).assert_status(204)
