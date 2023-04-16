import pytest

import data
from api.endpoints.items.facility_item_type_api import FacilityItemTypeAPI


@pytest.fixture()
def create_fake_facility_item_type_superuser(
    client,
    create_fake_facility,
    create_fake_inventory_item_type
):
    facility_item_id = -1

    def _fixture(**kwargs):
        # Create facility
        facility_payload, facility_response, facility_model = create_fake_facility()
        facility_id = facility_model.data.id

        # Create inventory item type
        inventory_item_payload, inventory_item_response, inventory_item_model = create_fake_inventory_item_type()
        inventory_item_type_id = inventory_item_model.data.id

        # Create facility item type
        payload = data.fake.model.facility_item_type(
            item_type_id=inventory_item_type_id,
            facility_id=facility_id,
            **kwargs
        )
        response, model = FacilityItemTypeAPI(client).create_item_type(data=payload)
        nonlocal facility_item_id
        facility_item_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        FacilityItemTypeAPI(client).delete_item_type(id=facility_item_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
