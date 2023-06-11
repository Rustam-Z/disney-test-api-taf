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

    def get_current_inventory(self, **kwargs) -> tuple:
        ...

    def get_daily_inventory(self, **kwargs) -> tuple:
        ...

    def get_daily_goals(self, **kwargs) -> tuple:
        ...

    def get_metro_locations(self, **kwargs) -> tuple:
        ...
