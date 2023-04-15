import pytest

import data
from api.endpoints.items.inventory_item_type_api import InventoryItemTypeAPI
from api.endpoints.items.inventory_category_api import InventoryCategoryAPI


@pytest.fixture()
def create_fake_inventory_item_type(client):
    category_id = -1
    item_type_id = -1

    def _fixture(**kwargs):
        # Setup
        payload = data.fake.model.inventory_category()
        response, model = InventoryCategoryAPI(client).create_category(data=payload)
        nonlocal category_id
        category_id = model.data.id

        # Create inventory item type
        payload = data.fake.model.inventory_item_type(category_id=category_id, **kwargs)
        response, model = InventoryItemTypeAPI(client).create_item_type(data=payload)

        if response.status_code in range(200, 300):
            nonlocal item_type_id
            item_type_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        InventoryItemTypeAPI(client).delete_item_type(id=item_type_id, expect_json=False)
        InventoryCategoryAPI(client).delete_category(id=category_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
