from api.enums.params import Param
from api.enums.sections import Section
from api.responses.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.responses.metro.metro_item_configuration_model import (
    GetAllConfigsSuccessResponse,
    GetConfigSuccessResponse,
    CreateConfigSuccessResponse,
    UpdateConfigSuccessResponse,
)


class MetroItemConfigurationAPI:
    METRO_ITEM_CONFIGURATION = '/metro/item-configuration/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.METRO_ITEM_CONFIGURATION.value
        }

    def get_all_configs(self, **kwargs) -> tuple:
        path = self.METRO_ITEM_CONFIGURATION
        response = self.client.get(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = GetAllConfigsSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_config(self, id: int, **kwargs) -> tuple:
        path = f'{self.METRO_ITEM_CONFIGURATION}{id}'
        response = self.client.get(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = GetConfigSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def create_config(self, data: dict, **kwargs) -> tuple:
        path = self.METRO_ITEM_CONFIGURATION
        response = self.client.post(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateConfigSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_config(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.METRO_ITEM_CONFIGURATION}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = UpdateConfigSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_config(self, id: int, **kwargs) -> tuple:
        path = f'{self.METRO_ITEM_CONFIGURATION}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = None  # Success response doesn't have body
        else:
            model = ErrorResponse(**response.json())

        return response, model
