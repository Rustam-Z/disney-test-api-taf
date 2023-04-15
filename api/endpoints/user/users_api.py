from string import Template

from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.user.users_model import (GetAllUsersSuccessResponse,
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

        if response.status_code in range(200, 300):
            model = GetAllUsersSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_user(self, id: int, **kwargs) -> tuple:
        path = f'{self.USERS}{id}'
        response = self.client.get(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = GetUserSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def create_user(self, data: dict, **kwargs) -> tuple:
        path = self.USERS
        response = self.client.post(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateUserSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_user(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.USERS}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = UpdateUserSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_user(self, id: int, **kwargs) -> tuple:
        path = f'{self.USERS}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = None
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_user_password(self, id: int, data: dict, **kwargs) -> tuple:
        path = self.UPDATE_USER_PASSWORD.substitute(user_id=id)
        response = self.client.post(path, data=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = response.json()
        else:
            model = ErrorResponse(**response.json())

        return response, model
