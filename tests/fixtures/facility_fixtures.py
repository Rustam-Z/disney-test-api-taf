import pytest

import data
from api.requests.customer_api import CustomerAPI
from api.requests.facility_api import FacilityAPI


@pytest.fixture()
def create_fake_facility(client):
    customers = []
    facility_id = -1

    def _fixture(no_of_customers: int = 0, **kwargs):
        # Create customers
        for _ in range(no_of_customers):
            payload = data.fake.model.customer()  # Request body JSON
            response, model = CustomerAPI(client).create_customer(data=payload)
            customers.append(model.data.id)

        # Create facility
        payload = data.fake.model.facility(customers=customers, **kwargs)  # Request body JSON
        response, model = FacilityAPI(client).create_facility(data=payload)

        if response.status_code in range(200, 300):
            nonlocal facility_id
            facility_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup, delete facility and customer
    try:
        FacilityAPI(client).delete_facility(id=facility_id, expect_json=False)
        for customer_id in customers:
            CustomerAPI(client).delete_customer(id=customer_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
