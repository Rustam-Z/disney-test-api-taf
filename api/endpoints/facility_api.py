from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.facility_models import (GetAllFacilitiesSuccessResponse,
                                                 GetFacilitySuccessResponse,
                                                 CreateFacilitySuccessResponse,
                                                 UpdateFacilitySuccessResponse,
                                                 )
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient


class FacilityAPI:
    FACILITY = '/facility/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.FACILITY.value
        }

    def get_all_facilities(self, **kwargs) -> tuple:
        path = self.FACILITY
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllFacilitiesSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_facility(self, id: int, **kwargs) -> tuple:
        path = f'{self.FACILITY}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetFacilitySuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_facility(self, data: dict, **kwargs) -> tuple:
        path = self.FACILITY
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateFacilitySuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_facility(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.FACILITY}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UpdateFacilitySuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_facility(self, id: int, **kwargs) -> tuple:
        path = f'{self.FACILITY}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
