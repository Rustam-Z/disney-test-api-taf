from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.metro.metro_models import (CreateMetroSuccessResponse,
                                                    UpdateMetroSuccessResponse,
                                                    GetMetroSuccessResponse,
                                                    GetAllMetrosSuccessResponse,
                                                    )
from api.response_models.response_models import ErrorResponse
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
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllMetrosSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_metro(self, id: int, **kwargs) -> tuple:
        path = f'{self.METRO}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetMetroSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_metro(self, data: dict, **kwargs) -> tuple:
        path = self.METRO
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateMetroSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_metro(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.METRO}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UpdateMetroSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_metro(self, id: int, **kwargs) -> tuple:
        path = f'{self.METRO}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
