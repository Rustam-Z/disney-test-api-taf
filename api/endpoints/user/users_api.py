from string import Template

from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.user.users_models import (GetAllUsersSuccessResponse,
                                                   GetUserSuccessResponse,
                                                   CreateUserSuccessResponse,
                                                   UpdateUserSuccessResponse
                                                   )


class UsersAPI:
    USERS = '/user/users/'
    UPDATE_USER_PASSWORD = Template(f'{USERS}$user_id/password/')

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.USERS.value
        }

    def get_all_users(self, params: dict = None, **kwargs) -> tuple:
        """
        NOTE!
        params = {
            Param.FACILITY.value,
            Param.SEARCH.value,
            Param.PAGE.value,
            Param.PAGE_SIZE.value,
        }
        """
        if params is None:
            params = {}

        params.update(self.params)  # Create query string params dict.

        path = self.USERS
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllUsersSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_user(self, id: int, **kwargs) -> tuple:
        path = f'{self.USERS}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetUserSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_user(self, data: dict, **kwargs) -> tuple:
        path = self.USERS
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateUserSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_user(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.USERS}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UpdateUserSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_user(self, id: int, **kwargs) -> tuple:
        path = f'{self.USERS}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_user_password(self, id: int, data: dict, **kwargs) -> tuple:
        path = self.UPDATE_USER_PASSWORD.substitute(user_id=id)
        response = self.client.post(path, data=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
