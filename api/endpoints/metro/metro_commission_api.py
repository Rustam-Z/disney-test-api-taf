from api.enums.params import Param
from api.enums.sections import Section
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse
from api.response_models.metro.metro_commission_models import (
    GetAllMetrosSuccessResponse,
    CreateMetroSuccessResponse,
)


class MetroCommissionAPI:
    METRO_COMMISSION = '/metro/commission/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.CUSTOMERS.value
        }

    def get_all_metros(self, **kwargs) -> tuple:
        path = self.METRO_COMMISSION
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllMetrosSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_metro(self, data: dict, **kwargs) -> tuple:
        path = self.METRO_COMMISSION
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateMetroSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def upload_csv(self):  # TODO
        ...
