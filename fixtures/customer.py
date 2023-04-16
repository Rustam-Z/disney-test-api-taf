import pytest

import data
from api.endpoints.customer_api import CustomerAPI


@pytest.fixture()
def create_fake_customer(client):
    """
    The decorator to create a fake entity (customer).

    Example usage:
        Use `request` argument in your tests.
        payload, response, model = request.getfixturevalue('create_fake_customer')()
    """
    customer_id = -1

    def _fixture(**kwargs):
        # Create customer
        payload = data.fake.model.customer(**kwargs)
        response, model = CustomerAPI(client).create_customer(data=payload)
        nonlocal customer_id
        customer_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        CustomerAPI(client).delete_customer(id=customer_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
