from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.customer.delivery_schedule_models import (
    GetDeliveryScheduleSuccessResponse,
    CreateDeliveryScheduleSuccessResponse,
    GetAllDeliveryScheduleSuccessResponse,
)


class DeliveryScheduleAPI:
    DELIVERY_SCHEDULE = '/customer/delivery-schedule/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.DELIVERY_SCHEDULE.value
        }

    def get_all_schedules(self, **kwargs) -> tuple:
        path = self.DELIVERY_SCHEDULE
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllDeliveryScheduleSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_schedule(self, id: int, **kwargs) -> tuple:
        path = f'{self.DELIVERY_SCHEDULE}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetDeliveryScheduleSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_schedule(self, data: dict, **kwargs) -> tuple:
        path = self.DELIVERY_SCHEDULE
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateDeliveryScheduleSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_schedule(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.DELIVERY_SCHEDULE}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = response.json()
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_schedule(self, id: int, **kwargs) -> tuple:
        path = f'{self.DELIVERY_SCHEDULE}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
