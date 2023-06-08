from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.staging.staging_models import (
    GetOrders,
    GetMetroList,
    AssignMetro, SubmitAction,
)


class StagingAPI:
    ORDERS = '/staging/'
    METRO_LIST = '/staging/metro-list/'
    METRO_ASSIGN = '/staging/metro-assign/'
    METRO_REMOVE = '/staging/metro-remove/'
    SUBMIT_ACTION = '/staging/submit-action/'
    METRO_CONFIG_DETAIL = '/staging/metro-config-detail/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.STAGING.value
        }

    def get_orders(self, params: dict = None, **kwargs) -> tuple:
        """
        Get all orders, get all orders by facility, get all facility orders by customer.
        Params: facility, customer_barcode, search, page, page_size.
        """
        if params is None:
            params = {}

        params.update(self.params)

        path = self.ORDERS
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetOrders(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_metro_list(self, params: dict = None, **kwargs) -> tuple:
        """
        Get metros list by order.
        Params: order_id.
        """
        if params is None:
            params = {}

        params.update(self.params)

        path = self.METRO_LIST
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetMetroList(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def assign_metro(self, data: dict, **kwargs) -> tuple:
        """
        Assign metro to order by order_id.
        """
        path = self.METRO_ASSIGN
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = AssignMetro(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def remove_metro(self, data: dict, **kwargs) -> tuple:
        """
        Unassign/remove metro from order by order_id.
        """
        path = self.METRO_REMOVE
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def submit_action(self, data: dict, **kwargs) -> tuple:
        path = self.SUBMIT_ACTION
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = SubmitAction(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_metro_item_config_detail(self, params: dict = None, **kwargs) -> tuple:
        """
        Get metros item configuration details.
        Params: config_qr_code.
        """
        if params is None:
            params = {}

        params.update(self.params)

        path = self.METRO_CONFIG_DETAIL
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
