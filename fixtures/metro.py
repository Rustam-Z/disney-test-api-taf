import pytest

import data
from api.endpoints.facility_api import FacilityAPI
from api.endpoints.metro.metro_api import MetroAPI
from api.endpoints.metro.metro_commission_api import MetroCommissionAPI


@pytest.fixture()
def create_fake_metro_for_commission_superuser(client):

    def _fixture(**kwargs):
        payload = data.fake.model.facility()
        response, model = FacilityAPI(client).create_facility(data=payload)
        facility_id = model.data.id

        # Create metro
        payload = data.fake.model.metro_for_commission(facility_id=facility_id, **kwargs)
        response, model = MetroCommissionAPI(client).create_metro(data=payload)

        return payload, response, model

    yield _fixture


@pytest.fixture()
def create_fake_metro_superuser(client):
    facility_id = -1
    metro_id = -1

    def _fixture(**kwargs):
        payload = data.fake.model.facility()
        response, model = FacilityAPI(client).create_facility(data=payload)
        nonlocal facility_id
        facility_id = model.data.id

        # Create metro
        payload = data.fake.model.metro(facility_id=facility_id, **kwargs)
        response, model = MetroAPI(client).create_metro(data=payload)
        nonlocal metro_id
        metro_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        MetroAPI(client).delete_metro(id=metro_id, expect_json=False)
        FacilityAPI(client).delete_facility(id=facility_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
