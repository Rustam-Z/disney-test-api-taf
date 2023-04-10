from api.enums.params import Param
from api.enums.sections import Section
from api.responses.metro_model import (CreateMetroSuccessResponse,
                                       UpdateMetroSuccessResponse,
                                       GetMetroSuccessResponse,
                                       GetAllMetrosSuccessResponse,
                                       )
from api.responses.response_models import ErrorResponse
from core.http_client import HTTPClient


class MetroAPI:
    METRO = '/metro/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.METRO.value
        }

    def get_all_metros(self, **kwargs) -> tuple:
        path = self.METRO
        response = self.client.get(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = GetAllMetrosSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_metro(self, id: int, **kwargs) -> tuple:
        path = f'{self.METRO}{id}'
        response = self.client.get(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = GetMetroSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def create_metro(self, data: dict, **kwargs) -> tuple:
        path = self.METRO
        response = self.client.post(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateMetroSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_metro(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.METRO}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = UpdateMetroSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_metro(self, id: int, **kwargs) -> tuple:
        path = f'{self.METRO}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = None
        else:
            model = ErrorResponse(**response.json())

        return response, model
