from core.http_client import HTTPClient
from api.responses.menu_model import MenuListSuccessResponse
from api.responses.response_models import ErrorResponse


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
