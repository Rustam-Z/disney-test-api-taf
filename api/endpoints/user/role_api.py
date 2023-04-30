from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.user.role_models import (
    GetRoleSuccessResponse,
    GetAllRolesSuccessResponse,
    CreateRoleSuccessResponse,
    UpdateRoleSuccessResponse,
)


class RoleAPI:
    ROLE = '/user/role/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.ROLES.value
        }

    def get_all_roles(self, params: dict = None, **kwargs) -> tuple:
        """
        NOTE!
        params = {
            Param.FACILITY.value,
            Param.SEARCH.value,
            Param.PAGE.value,
            Param.PAGE_SIZE.value,
            Param.IS_DRIVER.value,
        }
        """
        if params is None:
            params = {}

        params.update(self.params)  # Create query string params dict.

        path = self.ROLE
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllRolesSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_role(self, id: int, **kwargs) -> tuple:
        path = f'{self.ROLE}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetRoleSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_role(self, data: dict, **kwargs) -> tuple:
        path = self.ROLE
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateRoleSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_role(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.ROLE}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UpdateRoleSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_role(self, id: int, **kwargs) -> tuple:
        path = f'{self.ROLE}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
