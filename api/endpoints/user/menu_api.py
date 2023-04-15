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

        if response.status_code in range(200, 300):
            model = MenuListSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_user_menus(self, is_for_mobile: bool = False, **kwargs) -> tuple:
        params = {
            Param.IS_FOR_MOBILE.value: is_for_mobile
        }
        response = self.client.get(self.USER_MENUS, params=params, **kwargs)

        if response.status_code in range(200, 300):
            model = UserMenusSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model
