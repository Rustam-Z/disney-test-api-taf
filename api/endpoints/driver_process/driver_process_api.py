from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.driver_process.driver_process_models import (
    GetOrders,
    GetMetroList,
)


class DriverProcessAPI:
    ORDERS = '/driver-process/'
    METRO_LIST = '/driver-process/{order_id}/order-metros/'  # Is it order id?
    READER_METRO_SCAN = '/driver-process/reader-metro-scan/'
    DRIVER_METRO_SCAN = '/driver-process/driver-metro-scan/'
    _METRO_TRACKING = '/inventory/metro-tracking/'  # DEPRECATED!!!
    SUBMIT = '/driver-process/submit/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.STAGING.value
        }

    def get_orders(self, params: dict = None, **kwargs) -> tuple:
        """
        Params: action (pickup_at_facility, delivery_at_customer, delivery_at_facility),
                date_start_time_utc
                driver_id
                customer
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

    def get_metro_list(self, id: int, **kwargs) -> tuple:
        """
        Get metros list by order.
        """
        path = self.METRO_LIST.format(order_id=id)
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetMetroList(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def reader_metro_scan(self, data: dict, **kwargs) -> tuple:
        path = self.READER_METRO_SCAN
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def driver_metro_scan(self, data: dict, **kwargs) -> tuple:
        path = self.READER_METRO_SCAN
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def submit(self, data: dict, **kwargs) -> tuple:
        path = self.READER_METRO_SCAN
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
