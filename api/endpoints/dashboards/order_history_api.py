from api.enums.params import Param
from api.enums.sections import Section
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse


class OrderHistoryDashboardAPI:
    ORDER_HISTORY_LOGS = '/dashboard/order-history-logs/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.DASHBOARD.value
        }

    def get_order_history(self, params: dict = None, **kwargs) -> tuple:
        """
        Params:
        facility
        """
        if params is None:
            params = {}

        params.update(self.params)  # Create query string params dict.

        path = f'{self.ORDER_HISTORY_LOGS}order-history'
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_order_history_chart(self, params: dict = None, **kwargs) -> tuple:
        """
        Params:
        facility
        """
        if params is None:
            params = {}

        params.update(self.params)  # Create query string params dict.

        path = f'{self.ORDER_HISTORY_LOGS}order-history-chart'
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_order_metros(self, order_id: int, **kwargs) -> tuple:
        path = f'{self.ORDER_HISTORY_LOGS}{order_id}/order-metros'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_order_item_types(self, order_id: int, **kwargs) -> tuple:
        path = f'{self.ORDER_HISTORY_LOGS}{order_id}/order-item-types'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
