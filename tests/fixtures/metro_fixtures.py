import pytest

import data
from api.requests.facility_api import FacilityAPI
from api.requests.metro_api import MetroAPI


@pytest.fixture()
def create_fake_metro(client):
    facility_id = -1
    metro_id = -1

    def _fixture(**kwargs):
        # Setup
        payload = data.fake.model.facility()
        response, model = FacilityAPI(client).create_facility(data=payload)
        nonlocal facility_id
        facility_id = model.data.id

        # Create inventory item type
        payload = data.fake.model.metro(facility_id=facility_id, **kwargs)
        response, model = MetroAPI(client).create_metro(data=payload)

        if response.status_code in range(200, 300):
            nonlocal metro_id
            metro_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    MetroAPI(client).delete_metro(id=metro_id)
    FacilityAPI(client).delete_facility(id=facility_id)
