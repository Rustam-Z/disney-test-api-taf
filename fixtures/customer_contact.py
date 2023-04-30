import random

import pytest

import data
from api.endpoints.customer.customer_contact_api import CustomerContactAPI


@pytest.fixture()
def create_fake_customer_contact_superuser(client, create_fake_facility):
    customer_contact_id = -1

    def _fixture(**kwargs):
        # Arrange
        if 'facility_id' not in kwargs:
            facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
            kwargs['facility_id'] = facility_model.data.id
            kwargs['customer_id'] = random.choice(facility_model.data.customers)

        # Create customer contact
        payload = data.fake.model.customer_contact(**kwargs)
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
