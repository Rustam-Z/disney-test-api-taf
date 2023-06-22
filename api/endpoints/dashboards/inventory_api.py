from api.enums.params import Param
from api.enums.sections import Section
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse


class InventoryDashboardAPI:
    DASHBOARD = '/dashboard/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.DASHBOARD.value
        }

    def get_current_inventory(self, params: dict = None, **kwargs) -> tuple:
        """
        Params:
        facility: int
        inventory_base_filter: metro_config/item_type
        category_id: int
        item_type_ids[]: int
        item_type_ids[]: int
        metro_config_ids[]: int
        metro_config_ids[]: int
        filter_by_all: bool

        If filter_by_all is selected no need to select item type and metro config
        """
        if params is None:
            params = {}

        params.update(self.params)  # Create query string params dict.

        path = f'{self.DASHBOARD}current-inventory'
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_daily_inventory(self, params: dict = None, **kwargs) -> tuple:
        """
        Params:
        facility: int
        daily_inventory_type: cart_build/delivered
        inventory_base_filter: metro_config/item_type
        frequency: daily/weekly/monthly
        category_id: int
        item_type_ids[]: int
        item_type_ids[]: int
        metro_config_ids[]: int
        metro_config_ids[]: int
        filter_by_all: bool
        """
        if params is None:
            params = {}

        params.update(self.params)  # Create query string params dict.

        path = f'{self.DASHBOARD}daily-inventory'
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_daily_goals(self, params: dict = None, **kwargs) -> tuple:
        """
        Params:
        facility: int
        inventory_base_filter: metro_config/item_type
        frequency: daily/weekly/monthly
        category_id: int
        item_type_ids[]: int
        item_type_ids[]: int
        metro_config_ids[]: int
        metro_config_ids[]: int
        filter_by_all: bool ???
        """
        if params is None:
            params = {}

        params.update(self.params)  # Create query string params dict.

        path = f'{self.DASHBOARD}daily-inventory-goal'
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_metro_locations(self, params: dict = None, **kwargs) -> tuple:
        """
        Params:
        facility
        """
        if params is None:
            params = {}

        params.update(self.params)  # Create query string params dict.

        path = f'{self.DASHBOARD}metro-location'
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
