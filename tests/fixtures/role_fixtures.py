import pytest

import data
from api.requests.menu_api import MenuAPI
from api.requests.role_api import RoleAPI


@pytest.fixture()
def create_fake_role(client):
    role_id = -1

    def _fixture(**kwargs):
        # Create role request body_str
        menu_list_response, menu_list_model = MenuAPI(client).get_menu_list()
        payload = data.fake.model.role(sections=menu_list_model.data.results, **kwargs)

        # Create role
        response, model = RoleAPI(client).create_role(data=payload)

        if response.status_code in range(200, 300):
            nonlocal role_id
            role_id = model.data.id

        return payload, response, model

    yield _fixture

    # Cleanup
    try:
        RoleAPI(client).delete_role(id=role_id, expect_json=False)
    except Exception as e:
        print(f"Error: {e}")
