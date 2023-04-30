from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.user.drivers_list_models import GetAllDriversSuccessResponse
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse


class DriversListAPI:
    DRIVER_LIST = '/user/driver-list/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.USERS.value
        }

    def get_drivers_list(self, **kwargs) -> tuple:
        response = self.client.get(self.DRIVER_LIST, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllDriversSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
