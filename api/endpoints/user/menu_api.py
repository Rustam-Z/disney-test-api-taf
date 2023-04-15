from api.enums.params import Param
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse
from api.response_models.user.menu_models import (MenuListSuccessResponse,
                                                  UserMenusSuccessResponse,
                                                  )


class MenuAPI:
    MENU_LIST = '/user/menu-list/'
    USER_MENUS = '/user/user-menus/'

    def __init__(self, client: HTTPClient):
        self.client = client

    def get_menu_list(self, **kwargs) -> tuple:
        response = self.client.get(self.MENU_LIST, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = MenuListSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_user_menus(self, is_for_mobile: bool = False, **kwargs) -> tuple:
        params = {
            Param.IS_FOR_MOBILE.value: is_for_mobile
        }
        response = self.client.get(self.USER_MENUS, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UserMenusSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
