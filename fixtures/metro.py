import pytest

import data
from api.endpoints.metro.metro_api import MetroAPI
from api.endpoints.metro.metro_commission_api import MetroCommissionAPI


@pytest.fixture()
def create_fake_metro_for_commission_superuser(client, create_fake_facility):

    def _fixture(**kwargs):
        # Arrange
        if 'facility_id' not in kwargs:
            facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
            kwargs['facility_id'] = facility_model.data.id

        # Create metro
        payload = data.fake.model.metro_for_commission(**kwargs)
        response, model = MetroCommissionAPI(client).create_metro(data=payload)

        return payload, response, model

    yield _fixture


@pytest.fixture()
def create_fake_metro_superuser(client, create_fake_facility):
    metro_id = -1

    def _fixture(**kwargs):
        # Arrange
        if 'facility_id' not in kwargs:
            facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
            kwargs['facility_id'] = facility_model.data.id

        # Create metro
        payload = data.fake.model.metro(**kwargs)
        response, model = MetroAPI(client).create_metro(data=payload)
        nonlocal metro_id
        metro_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        MetroAPI(client).delete_metro(id=metro_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
