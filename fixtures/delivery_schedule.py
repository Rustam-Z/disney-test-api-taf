import random

import pytest

import data
from api.endpoints.customer.delivery_schedule_api import DeliveryScheduleAPI


@pytest.fixture()
def create_fake_schedule_superuser(client, create_fake_facility):
    delivery_schedule_id = -1

    def _fixture(**kwargs):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
        facility_id = facility_model.data.id
        customer_id = random.choice(facility_model.data.customers)

        # Create cart
        payload = data.fake.model.delivery_schedule(facility_id=facility_id, customer_id=customer_id, **kwargs)
        response, model = DeliveryScheduleAPI(client).create_schedule(data=payload)
        nonlocal delivery_schedule_id
        delivery_schedule_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        DeliveryScheduleAPI(client).delete_schedule(id=delivery_schedule_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
