from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.customer_models import (CreateCustomerSuccessResponse,
                                                 GetAllCustomersSuccessResponse, GetCustomerSuccessResponse,
                                                 UpdateCustomerSuccessResponse,
                                                 )
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient


class CustomerAPI:
    CUSTOMER = '/customer/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.CUSTOMERS.value
        }

    def get_all_customers(self, **kwargs) -> tuple:
        path = self.CUSTOMER
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllCustomersSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_customer(self, id: int, **kwargs) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetCustomerSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_customer(self, data: dict, **kwargs) -> tuple:
        path = self.CUSTOMER
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateCustomerSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_customer(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UpdateCustomerSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_customer(self, id: int, **kwargs) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
