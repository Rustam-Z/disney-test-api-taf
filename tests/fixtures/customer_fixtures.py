import pytest

import data
from api.requests.customer_api import CustomerAPI


@pytest.fixture()
def create_fake_customer(client):
    customer_id = -1

    def _fixture(**kwargs):
        # Crete customer
        payload = data.fake.model.customer(**kwargs)  # Request body JSON
        response, model = CustomerAPI(client).create_customer(data=payload)

        if response.status_code in range(200, 300):
            nonlocal customer_id
            customer_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        CustomerAPI(client).delete_customer(id=customer_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
