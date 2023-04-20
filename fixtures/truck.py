import random

import pytest

import data
from api.endpoints.facility.truck_api import TruckAPI


@pytest.fixture()
def create_fake_truck(client, create_fake_facility):
    truck_id = -1

    def _fixture(**kwargs):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
        facility_id = facility_model.data.id

        # Create truck
        payload = data.fake.model.truck(facility_id=facility_id, **kwargs)
        response, model = TruckAPI(client).create_truck(data=payload)
        nonlocal truck_id
        truck_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        TruckAPI(client).delete_truck(id=truck_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
