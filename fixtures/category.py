import pytest

import data
from api.endpoints.items.inventory_category_api import InventoryCategoryAPI


@pytest.fixture()
def create_fake_inventory_category(client):
    category_id = -1

    def _fixture(**kwargs):
        # Create category
        payload = data.fake.model.inventory_category(**kwargs)
        response, model = InventoryCategoryAPI(client).create_category(data=payload)
        nonlocal category_id
        category_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        InventoryCategoryAPI(client).delete_category(id=category_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
