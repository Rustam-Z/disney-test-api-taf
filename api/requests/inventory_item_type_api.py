from api.enums.params import Param
from api.enums.sections import Section
from api.responses.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.responses.inventory_item_type_model import CreateInventoryItemTypeSuccessResponse


class InventoryItemTypeAPI:
    INVENTORY_ITEM_TYPE = '/inventory/item-type/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.INVENTORY_ITEM_TYPE.value
        }

    def create_item_type(self, data: dict) -> tuple:
        path = self.INVENTORY_ITEM_TYPE
        response = self.client.post(path, data=data, params=self.params)

        if response.status_code in range(200, 300):
            model = CreateInventoryItemTypeSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_item_type(self, id: int) -> tuple:
        path = f'{self.INVENTORY_ITEM_TYPE}{id}'
        response = self.client.delete(path, params=self.params)

        if response.status_code in range(200, 300):
            model = None
        else:
            model = ErrorResponse(**response.json())

        return response, model
