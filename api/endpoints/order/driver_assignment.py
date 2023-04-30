from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.order.driver_assignment_models import (
    GetUnassignedOrders,
    GetTruckOrdersAndDrivers,
    AssignDriversAndOrders,
)


class DriverAssignmentAPI:
    TRUCK_ORDERS_AND_DRIVERS = '/order/truck-orders-and-drivers/'
    UNASSIGNED_ORDERS = '/order/unassigned-orders/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.DRIVER_ASSIGNMENT.value
        }

    def get_unassigned_orders(self, params: dict = None, **kwargs) -> tuple:
        if params is None:
            params = {}

        params.update(self.params)

        path = self.UNASSIGNED_ORDERS
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetUnassignedOrders(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_truck_orders_and_drivers(self, params: dict = None, **kwargs) -> tuple:
        if params is None:
            params = {}

        params.update(self.params)

        path = self.TRUCK_ORDERS_AND_DRIVERS
        response = self.client.get(path, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetTruckOrdersAndDrivers(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def assign_drivers_and_drivers(self, data: dict, params: dict = None, **kwargs) -> tuple:
        if params is None:
            params = {}

        params.update(self.params)

        path = self.TRUCK_ORDERS_AND_DRIVERS
        response = self.client.post(path, json=data, params=params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = AssignDriversAndOrders(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
