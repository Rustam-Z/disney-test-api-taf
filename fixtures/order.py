import random

import pytest

import data
from api.endpoints.order.order_api import OrderAPI


@pytest.fixture()
def create_fake_order(client, create_fake_facility):
    order_id = -1

    def _fixture(**kwargs):
        # Arrange
        if 'facility_id' not in kwargs:
            facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
            kwargs['facility_id'] = facility_model.data.id
            kwargs['customer_id'] = random.choice(facility_model.data.customers)

        # Create order
        payload = data.fake.model.order(**kwargs)
        response, model = OrderAPI(client).create_order(data=payload)
        nonlocal order_id
        order_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        OrderAPI(client).delete_order(id=order_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
