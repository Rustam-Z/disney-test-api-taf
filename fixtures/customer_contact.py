import random

import pytest

import data
from api.endpoints.customer.customer_contact_api import CustomerContactAPI


@pytest.fixture()
def create_fake_customer_contact(client, create_fake_facility):
    customer_contact_id = -1

    def _fixture(**kwargs):
        # Arrange
        facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
        facility_id = facility_model.data.id
        customer_id = random.choice(facility_model.data.customers)

        # Create customer contact
        payload = data.fake.model.customer_contact(facility_id=facility_id, customer_id=customer_id, **kwargs)
        response, model = CustomerContactAPI(client).create_customer_contact(data=payload)
        nonlocal customer_contact_id
        customer_contact_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        CustomerContactAPI(client).delete_customer_contact(id=customer_contact_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
