from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.inventory.inventory_location_models import (
    GetInventoryLocationSuccessResponse,
    GetAllInventoryLocationSuccessResponse,
    CreateInventoryLocationSuccessResponse,
    UpdateInventoryLocationSuccessResponse,
)


class InventoryLocationAPI:
    INVENTORY_LOCATION = '/inventory/location/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.INVENTORY_LOCATION.value
        }

    def get_all_inventoryLocations(self, **kwargs) -> tuple:
        path = self.INVENTORY_LOCATION
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllInventoryLocationSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_inventoryLocation(self, id: int, **kwargs) -> tuple:
        path = f'{self.INVENTORY_LOCATION}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetInventoryLocationSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_inventoryLocation(self, data: dict, **kwargs) -> tuple:
        path = self.INVENTORY_LOCATION
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateInventoryLocationSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_inventoryLocation(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.INVENTORY_LOCATION}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UpdateInventoryLocationSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_inventoryLocation(self, id: int, **kwargs) -> tuple:
        path = f'{self.INVENTORY_LOCATION}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
