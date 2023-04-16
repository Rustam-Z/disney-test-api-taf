import pytest

import data
from api.endpoints.items.inventory_item_type_api import InventoryItemTypeAPI


@pytest.fixture()
def create_fake_inventory_item_type(client, create_fake_inventory_category):
    item_type_id = -1

    def _fixture(**kwargs):
        # Setup
        payload, response, model = create_fake_inventory_category()
        category_id = model.data.id

        # Create inventory item type
        payload = data.fake.model.inventory_item_type(category_id=category_id, **kwargs)
        response, model = InventoryItemTypeAPI(client).create_item_type(data=payload)
        nonlocal item_type_id
        item_type_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        InventoryItemTypeAPI(client).delete_item_type(id=item_type_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
