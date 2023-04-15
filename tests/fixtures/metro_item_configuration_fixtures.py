import pytest

import data
from api.requests.facility_api import FacilityAPI
from api.requests.items.inventory_item_type_api import InventoryItemTypeAPI
from api.requests.items.inventory_category_api import InventoryCategoryAPI
from api.requests.items.facility_item_type_api import FacilityItemTypeAPI
from api.requests.metro.metro_item_configuration_api import MetroItemConfigurationAPI


@pytest.fixture()
def create_fake_metro_item_configuration_superuser(client):
    facility_id = -1
    category_id = -1
    inventory_item_type_id = -1
    facility_item_type_id = -1
    metro_item_config_id = -1

    def _fixture(**kwargs):
        # Setup
        # Create facility
        facility_payload = data.fake.model.facility()
        facility_response, facility_model = FacilityAPI(client).create_facility(data=facility_payload)
        nonlocal facility_id
        facility_id = facility_model.data.id

        # Create inventory category
        category_payload = data.fake.model.inventory_category()
        category_response, category_model = InventoryCategoryAPI(client).create_category(data=category_payload)
        nonlocal category_id
        category_id = category_model.data.id

        # Create inventory item type
        inventory_item_type_payload = data.fake.model.inventory_item_type(category_id=category_id)
        inventory_item_type_response, inventory_item_type_model = InventoryItemTypeAPI(client).create_item_type(
            data=inventory_item_type_payload
        )
        nonlocal inventory_item_type_id
        inventory_item_type_id = inventory_item_type_model.data.id

        # Create facility item type
        payload = data.fake.model.facility_item_type(item_type_id=inventory_item_type_id, facility_id=facility_id)
        response, model = FacilityItemTypeAPI(client).create_item_type(data=payload)
        nonlocal facility_item_type_id
        facility_item_type_id = model.data.id

        # Create metro item configuration
        payload = data.fake.model.metro_item_configuration(
            facility_id=facility_id,
            facility_item_type_ids=[facility_item_type_id],
            **kwargs
        )
        response, model = MetroItemConfigurationAPI(client).create_config(data=payload)
        nonlocal metro_item_config_id
        metro_item_config_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        MetroItemConfigurationAPI(client).delete_config(id=metro_item_config_id, expect_json=False)
        FacilityItemTypeAPI(client).delete_item_type(id=facility_item_type_id, expect_json=False)
        InventoryItemTypeAPI(client).delete_item_type(id=inventory_item_type_id, expect_json=False)
        InventoryCategoryAPI(client).delete_category(id=category_id, expect_json=False)
        FacilityAPI(client).delete_facility(id=facility_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
