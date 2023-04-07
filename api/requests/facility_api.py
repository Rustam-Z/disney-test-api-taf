from api.enums.params import Param
from api.enums.sections import Section
from api.responses.facility_model import (GetAllFacilitiesSuccessResponse,
                                          GetFacilitySuccessResponse,
                                          CreateFacilitySuccessResponse,
                                          UpdateFacilitySuccessResponse,
                                          )
from api.responses.response_models import ErrorResponse
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
        response = self.client.post(path, data=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateFacilitySuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_facility(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.FACILITY}{id}'
        response = self.client.patch(path, data=data, params=self.params, **kwargs)

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

    def send_request_without_section_param(
        self, method: str,
        id: int = None,
        is_error: bool = True,
        **kwargs
    ):
        # TODO: think about logic for tests without section
        path = f'{self.FACILITY}{id}' if id else self.FACILITY
        response = self.client.send_request(method, path, **kwargs)
        model = ErrorResponse(**response.json()) if is_error else response.json()

        return response, model
