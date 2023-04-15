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

        if response.status_code in range(200, 300):
            model = GetAllFacilitiesSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_facility(self, id: int, **kwargs) -> tuple:
        path = f'{self.FACILITY}{id}'
        response = self.client.get(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = GetFacilitySuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def create_facility(self, data: dict, **kwargs) -> tuple:
        path = self.FACILITY
        response = self.client.post(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateFacilitySuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_facility(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.FACILITY}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = UpdateFacilitySuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_facility(self, id: int, **kwargs) -> tuple:
        path = f'{self.FACILITY}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = None
        else:
            model = ErrorResponse(**response.json())

        return response, model
