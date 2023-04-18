import random

import pytest

import data
from api.endpoints.order.order_api import OrderAPI


@pytest.fixture()
def create_fake_order(client, create_fake_facility):
    delivery_schedule_id = -1

    def _fixture(**kwargs):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
        facility_id = facility_model.data.id
        customer_id = random.choice(facility_model.data.customers)

        # Create cart
        payload = data.fake.model.order(facility_id=facility_id, customer_id=customer_id, **kwargs)
        response, model = OrderAPI(client).create_order(data=payload)
        order_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        OrderAPI(client).delete_order(id=delivery_schedule_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
