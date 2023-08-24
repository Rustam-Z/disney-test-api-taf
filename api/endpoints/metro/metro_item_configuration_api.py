from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.metro.metro_item_configuration_models import (
    GetAllConfigsSuccessResponse,
    GetConfigSuccessResponse,
    CreateConfigSuccessResponse,
    UpdateConfigSuccessResponse,
)


class MetroItemConfigurationAPI:
    PRODUCT_CODE = '/metro/item-configuration/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.PRODUCT_CODE.value
        }

    def get_all_configs(self, **kwargs) -> tuple:
        path = self.PRODUCT_CODE
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllConfigsSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_config(self, id: int, **kwargs) -> tuple:
        path = f'{self.PRODUCT_CODE}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetConfigSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_config(self, data: dict, **kwargs) -> tuple:
        path = self.PRODUCT_CODE
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateConfigSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_config(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.PRODUCT_CODE}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UpdateConfigSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_config(self, id: int, **kwargs) -> tuple:
        path = f'{self.PRODUCT_CODE}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
