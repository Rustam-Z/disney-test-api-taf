from api.enums.params import Param
from api.enums.sections import Section
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse


class OrderHistoryDashboardAPI:
    DASHBOARD = '/dashboard/order-history-logs/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.DASHBOARD.value
        }

    def get_order_history(self, **kwargs) -> tuple:
        ...

    def get_order_history_chart(self, **kwargs) -> tuple:
        ...

    def get_order_metros(self, **kwargs) -> tuple:
        ...

    def get_order_item_types(self, **kwargs) -> tuple:
        ...
