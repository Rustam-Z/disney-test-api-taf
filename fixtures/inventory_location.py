import random

import pytest

import data
from api.endpoints.inventory.inventory_location_api import InventoryLocationAPI


@pytest.fixture()
def create_fake_inventory_location(client, create_fake_facility):
    inventory_location_id = -1

    def _fixture(**kwargs):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
        facility_id = facility_model.data.id


        # Create order
        payload = data.fake.model.inventory_location(facility_id=facility_id, **kwargs)
        response, model = InventoryLocationAPI(client).create_inventoryLocation(data=payload)
        nonlocal inventory_location_id
        inventory_location_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        InventoryLocationAPI(client).delete_inventoryLocation(id=inventory_location_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
