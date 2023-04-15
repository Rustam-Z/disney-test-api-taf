from api.enums.params import Param
from api.enums.sections import Section
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse
from api.response_models.metro.metro_commission_model import (
    GetAllMetrosSuccessResponse,
    CreateMetroResponse,
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

        if response.status_code in range(200, 300):
            model = GetAllMetrosSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def create_metro(self, data: dict, **kwargs) -> tuple:
        path = self.METRO_COMMISSION
        response = self.client.post(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateMetroResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def upload_csv(self):  # TODO
        ...
