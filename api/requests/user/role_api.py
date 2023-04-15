from api.enums.params import Param
from api.enums.sections import Section
from api.responses.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.responses.user.role_model import (GetRoleSuccessResponse,
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

        if response.status_code in range(200, 300):
            model = GetAllRolesSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_role(self, id: int, **kwargs) -> tuple:
        path = f'{self.ROLE}{id}'
        response = self.client.get(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = GetRoleSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def create_role(self, data: dict, **kwargs) -> tuple:
        path = self.ROLE
        response = self.client.post(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateRoleSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_role(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.ROLE}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = UpdateRoleSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_role(self, id: int, **kwargs) -> tuple:
        path = f'{self.ROLE}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = None
        else:
            model = ErrorResponse(**response.json())

        return response, model
