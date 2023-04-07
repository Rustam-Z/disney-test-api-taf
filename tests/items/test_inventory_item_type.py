"""
TODO:
- Test CRUD
    - Create with existing name
    - Create with not existing category id
    - Create without description, expected: item should be created
- Auth
- Section
"""

import data
from api.requests.inventory_category_api import InventoryCategoryAPI
from api.requests.inventory_item_type_api import InventoryItemTypeAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
from tests.fixtures.inventory_item_type_fixtures import create_fake_inventory_item_type


class TestInventoryCategoryCRUD:
    @users(User.SUPERUSER)
    def test_superUserCreatesItemType_returns201AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_inventory_item_type')()
        APIResponse(response).check_status(201)
        assert model.data.name == payload.get('name')

    @users(User.SUPERUSER)
    def test_superUserDeletesItemType_returns204(self, client, user):
        # Setup
        category_payload = data.fake.model.inventory_category()
        category_response, category_model = InventoryCategoryAPI(client).create_category(data=category_payload)
        category_id = category_model.data.id

        payload = data.fake.model.inventory_item_type(category_id=category_id)
        response, model = InventoryItemTypeAPI(client).create_item_type(data=payload)
        item_type_id = model.data.id

        # Act and assert
        response, _ = InventoryItemTypeAPI(client).delete_item_type(id=item_type_id)
        APIResponse(response).check_status(204)

        # Cleanup
        InventoryCategoryAPI(client).delete_category(id=category_id)
