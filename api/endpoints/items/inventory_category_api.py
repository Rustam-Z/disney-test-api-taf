from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.items.inventory_category_model import CreateInventoryCategorySuccessResponse


class InventoryCategoryAPI:
    INVENTORY_CATEGORY = '/inventory/category/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.INVENTORY_CATEGORY.value
        }

    def create_category(self, data: dict, **kwargs) -> tuple:
        path = self.INVENTORY_CATEGORY
        response = self.client.post(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateInventoryCategorySuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_category(self, id: int, **kwargs) -> tuple:
        path = f'{self.INVENTORY_CATEGORY}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = None
        else:
            model = ErrorResponse(**response.json())

        return response, model
