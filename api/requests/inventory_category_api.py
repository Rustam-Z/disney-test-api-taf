from api.enums.params import Param
from api.enums.sections import Section
from api.responses.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.responses.inventory_category_model import CreateInventoryCategorySuccessResponse


class InventoryCategoryAPI:
    INVENTORY_CATEGORY = '/inventory/category/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.INVENTORY_CATEGORY.value
        }

    def create_category(self, data: dict) -> tuple:
        path = self.INVENTORY_CATEGORY
        response = self.client.post(path, data=data, params=self.params)

        if response.status_code in range(200, 300):
            model = CreateInventoryCategorySuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_category(self, id: int) -> tuple:
        path = f'{self.INVENTORY_CATEGORY}{id}'
        response = self.client.delete(path, params=self.params)

        if response.status_code in range(200, 300):
            model = None
        else:
            model = ErrorResponse(**response.json())

        return response, model
