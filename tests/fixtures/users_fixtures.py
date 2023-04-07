import pytest

import data
from api.requests.customer_api import CustomerAPI
from api.requests.facility_api import FacilityAPI
from api.requests.menu_api import MenuAPI
from api.requests.role_api import RoleAPI
from api.requests.users_api import UsersAPI


@pytest.fixture()
def create_fake_user(client):
    """
    For superuser.

    To create a user we need to create a role.
    To create a role we need to create a facility, and assign role to facility.
    To create a facility we need to create its customers.
    """
    user_id = -1
    role_id = -1
    customer_id = -1
    facility_id = -1

    def _fixture(**kwargs):
        # Create customer
        customer_payload = data.fake.model.customer()
        customer_response, customer_model = CustomerAPI(client).create_customer(data=customer_payload)
        nonlocal customer_id
        customer_id = customer_model.data.id

        # Create facility
        facility_payload = data.fake.model.facility(customers=[customer_id])
        facility_response, facility_model = FacilityAPI(client).create_facility(data=facility_payload)
        nonlocal facility_id
        facility_id = facility_model.data.id

        # Fetch menu list, to give permission to user
        menu_list_response, menu_list_model = MenuAPI(client).get_menu_list()

        # Create a role
        role_payload = data.fake.model.role(sections=menu_list_model.data.results, facility_id=facility_id)
        role_response, role_model = RoleAPI(client).create_role(data=role_payload)
        nonlocal role_id
        role_id = role_model.data.id

        # Create user
        payload = data.fake.model.user(role_id=role_id, facility_id=facility_id, **kwargs)
        response, model = UsersAPI(client).create_user(data=payload)

        if response.status_code in range(200, 300):
            nonlocal user_id
            user_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        FacilityAPI(client).delete_facility(id=facility_id)
        CustomerAPI(client).delete_customer(id=customer_id)
        RoleAPI(client).delete_role(id=role_id)
        UsersAPI(client).delete_user(id=user_id)
    except Exception as e:
        print(f"Error: {e}")


@pytest.fixture()
def create_fake_user_without_facility(client):
    user_id = -1
    role_id = -1

    def _fixture(**kwargs):
        # Fetch menu list, to give permission to user
        menu_list_response, menu_list_model = MenuAPI(client).get_menu_list()

        # Create a role
        role_payload = data.fake.model.role(sections=menu_list_model.data.results)
        role_response, role_model = RoleAPI(client).create_role(data=role_payload)
        nonlocal role_id
        role_id = role_model.data.id

        # Create user
        payload = data.fake.model.user(role_id=role_id, **kwargs)
        response, model = UsersAPI(client).create_user(data=payload)

        if response.status_code in range(200, 300):
            nonlocal user_id
            user_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        RoleAPI(client).delete_role(id=role_id, expect_json=False)
        UsersAPI(client).delete_user(id=user_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
