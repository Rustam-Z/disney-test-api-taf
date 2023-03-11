from api.enums.params import Param
from api.enums.sections import Section
from core.http_client import HTTPClient


class FacilityAPI:
    FACILITY = '/facility/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.FACILITY.value
        }

    def get_all_facilities(self) -> tuple:
        path = self.FACILITY
        response = self.client.get(path, params=self.params)
        model = response.json()

        return response, model

    def get_facility(self, id: int) -> tuple:
        path = f'{self.FACILITY}{id}'
        response = self.client.get(path, params=self.params)
        model = response.json()

        return response, model

    def create_facility(self) -> tuple:
        ...

    def update_facility(self) -> tuple:
        ...

    def delete_facility(self) -> tuple:
        ...
