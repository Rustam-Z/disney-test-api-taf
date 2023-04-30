import pytest

import data
from api.endpoints.user.users_api import UsersAPI


@pytest.fixture()
def create_fake_user_superuser(client, create_fake_facility, create_fake_role):
    """
    For superuser.

    To create a user we need to create a role.
    To create a role we need to create a facility, and assign role to facility.
    To create a facility we need to create its customers.
    """
    user_id = -1

    def _fixture(**kwargs):
        # Arrange
        if 'facility_id' not in kwargs:
            facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
            kwargs['facility_id'] = facility_model.data.id

        if 'role_id' not in kwargs:
            role_payload, role_response, role_model = create_fake_role(facility_id=kwargs.get('facility_id'))
            kwargs['role_id'] = role_model.data.id

        # Create user
        payload = data.fake.model.user(**kwargs)
        response, model = UsersAPI(client).create_user(data=payload)
        nonlocal user_id
        user_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        UsersAPI(client).delete_user(id=user_id)
    except Exception as e:
        print(f"Error: {e}")


@pytest.fixture()
def create_fake_user(client, create_fake_role):
    user_id = -1

    def _fixture(**kwargs):
        # Arrange
        if 'role_id' not in kwargs:
            role_payload, role_response, role_model = create_fake_role()
            kwargs['role_id'] = role_model.data.id

        # Create user
        payload = data.fake.model.user(**kwargs)
        response, model = UsersAPI(client).create_user(data=payload)
        nonlocal user_id
        user_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        UsersAPI(client).delete_user(id=user_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
