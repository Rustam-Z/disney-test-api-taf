import pytest

import data
from api.endpoints.inventory.inventory_location_api import InventoryLocationAPI


@pytest.fixture()
def create_fake_inventory_location_superuser(client, create_fake_facility):
    inventory_location_id = -1

    def _fixture(**kwargs):
        # Arrange
        if 'facility_id' not in kwargs:
            facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
            kwargs['facility_id'] = facility_model.data.id

        # Create inventory location
        payload = data.fake.model.inventory_location(**kwargs)
        response, model = InventoryLocationAPI(client).create_inventory_location(data=payload)
        nonlocal inventory_location_id
        inventory_location_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        InventoryLocationAPI(client).delete_inventory_location(id=inventory_location_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
