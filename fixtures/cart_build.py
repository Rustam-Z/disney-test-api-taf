import pytest

import data
from api.endpoints.metro.cart_build_api import CartBuildAPI
from api.endpoints.items.inventory_item_type_api import InventoryItemTypeAPI
from api.endpoints.items.inventory_category_api import InventoryCategoryAPI
from api.endpoints.items.facility_item_type_api import FacilityItemTypeAPI
from api.endpoints.metro.metro_api import MetroAPI
from api.endpoints.metro.metro_item_configuration_api import MetroItemConfigurationAPI


@pytest.fixture()
def create_fake_cart_superuser(client, create_fake_facility):
    category_id = -1
    inventory_item_type_id = -1
    facility_item_type_id = -1
    metro_item_config_id = -1
    metro_id = -1

    def _fixture(**kwargs):
        # Arrange

        # Create facility
        if 'facility_id' not in kwargs:
            facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
            kwargs['facility_id'] = facility_model.data.id
        facility_id = kwargs['facility_id']

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
        )
        response, conf_model = MetroItemConfigurationAPI(client).create_config(data=payload)
        nonlocal metro_item_config_id
        metro_item_config_id = conf_model.data.id

        # Create metro
        payload = data.fake.model.metro(facility_id=facility_id)
        response, metro_model = MetroAPI(client).create_metro(data=payload)
        nonlocal metro_id
        metro_id = metro_model.data.id

        # Create cart
        metro_qr_code = metro_model.data.qr_code
        metro_config_qr_code = conf_model.data.qr_code
        payload = data.fake.model.cart(metro_qr_code=metro_qr_code, metro_config_qr_code=metro_config_qr_code, **kwargs)
        response, model = CartBuildAPI(client).create_cart(data=payload)

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        MetroAPI(client).delete_metro(id=metro_id, expect_json=False)
        MetroItemConfigurationAPI(client).delete_config(id=metro_item_config_id, expect_json=False)
        FacilityItemTypeAPI(client).delete_item_type(id=facility_item_type_id, expect_json=False)
        InventoryItemTypeAPI(client).delete_item_type(id=inventory_item_type_id, expect_json=False)
        InventoryCategoryAPI(client).delete_category(id=category_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
