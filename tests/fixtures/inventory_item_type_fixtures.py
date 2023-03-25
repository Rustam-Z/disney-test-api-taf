import pytest

import data
from api.requests.inventory_item_type_api import InventoryItemTypeAPI
from api.requests.inventory_category_api import InventoryCategoryAPI


@pytest.fixture()
def create_fake_facility(client):
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
    InventoryItemTypeAPI(client).delete_item_type(id=item_type_id)
    InventoryCategoryAPI(client).delete_category(id=category_id)
