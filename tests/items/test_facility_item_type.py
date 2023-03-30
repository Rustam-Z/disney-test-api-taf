"""
TODO:
- Test CRUD
    - Create with existing name
    - Create with not existing category id and inventory item type
    - Create without description, expected: item should be created
- Auth
- Section
"""

from core.api_response import APIResponse
from core.decorators import users
from core.enums.users import User
from api.requests.facility_item_type_api import FacilityItemTypeAPI
from tests.fixtures.facility_item_type_fixtures import create_fake_facility_item_type


class TestInventoryCategoryCRUD:
    @users(User.SUPERUSER)
    def test_superUserCreatesItemType_returns201AndData(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_facility_item_type')()
        APIResponse(response).check_status(201)
        assert model.data.name == payload.get('name')

    @users(User.SUPERUSER)
    def test_superUserDeletesItemType_returns204(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_facility_item_type')()
        existing_id = model.data.id

        # Act and assert
        response, _ = FacilityItemTypeAPI(client).delete_item_type(id=existing_id)
        APIResponse(response).check_status(204)
        # NOTE! In teardown stage deletion will return 4xx error, because we already deleted this item.
