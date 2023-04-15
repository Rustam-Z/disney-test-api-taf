from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.items.facility_item_type_models import CreateFacilityItemTypeSuccessResponse


class FacilityItemTypeAPI:
    FACILITY_ITEM_TYPE = '/inventory/facility-item-type/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.INVENTORY_ITEM_TYPE.value
        }

    def create_item_type(self, data: dict, **kwargs) -> tuple:
        path = self.FACILITY_ITEM_TYPE
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateFacilityItemTypeSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_item_type(self, id: int, **kwargs) -> tuple:
        path = f'{self.FACILITY_ITEM_TYPE}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 204:
            response_payload = None
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload