from api.enums.params import Param
from core.http_client import HTTPClient
from api.responses.response_models import ErrorResponse
from api.responses.menu_model import (MenuListSuccessResponse,
                                      UserMenusSuccessResponse,
                                      )


class MenuAPI:
    MENU_LIST = '/user/menu-list/'
    USER_MENUS = '/user/user-menus/'

    def __init__(self, client: HTTPClient):
        self.client = client

    def get_menu_list(self) -> tuple:
        response = self.client.get(self.MENU_LIST)

        if response.status_code == 200:
            model = MenuListSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_user_menus(self, is_for_mobile: bool = False) -> tuple:
        params = {
            Param.IS_FOR_MOBILE.value: is_for_mobile
        }
        response = self.client.get(self.USER_MENUS, params=params)

        if response.status_code == 200:
            model = UserMenusSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model
