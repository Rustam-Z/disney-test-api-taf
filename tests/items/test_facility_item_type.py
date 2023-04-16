from core.asserters import APIResponse
from core.decorators import users
from core.enums.users import User
from api.endpoints.items.facility_item_type_api import FacilityItemTypeAPI


class TestCreateFacilityItemType:
    @users(User.SUPERUSER)
    def test_createFacilityItemTypeBySuperuser_withValidData_returns201AndData(self, client, user, request):
        # Act
        payload, response, model = request.getfixturevalue('create_fake_facility_item_type_superuser')()

        # Assert
        APIResponse(response).assert_status(201)
        APIResponse(response).assert_models(payload)


class TestDeleteFacilityItemType:
    @users(User.SUPERUSER)
    def test_deleteFacilityItemTypeBySuperuser_withValidID_returns204(self, client, user, request):
        # Arrange
        payload, response, model = request.getfixturevalue('create_fake_facility_item_type_superuser')()
        existing_id = model.data.id

        # Act
        response, model = FacilityItemTypeAPI(client).delete_item_type(id=existing_id)

        # Assert
        APIResponse(response).assert_status(204)
