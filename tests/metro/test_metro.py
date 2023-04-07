from api.requests.metro_api import MetroAPI
from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
from tests.fixtures.metro_fixtures import create_fake_metro


class TestMetroCRUD:
    @users(User.SUPERUSER)
    def test_createNewMetro_returns201AndData(self, client, user, request):
        # Act and assert
        payload, response, model = request.getfixturevalue('create_fake_metro')()
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_body(payload)

    @users(User.SUPERUSER)
    def test_deleteMetro_returns204(self, client, user, request):
        # Setup
        payload, response, model = request.getfixturevalue('create_fake_metro')()
        existing_id = model.data.id

        # Act and assert
        response, _ = MetroAPI(client).delete_metro(id=existing_id)
        APIResponse(response).assert_status(204)
        # NOTE! In teardown stage deletion will return 4xx error, because we already deleted this item.
