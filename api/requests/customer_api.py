from api.enums.params import Param
from api.enums.sections import Section
from api.responses.customer_model import (CreateCustomerSuccessResponse,
                                          GetAllCustomersSuccessResponse, GetCustomerSuccessResponse,
                                          UpdateCustomerSuccessResponse,
                                          )
from api.responses.response_models import ErrorResponse
from core.http_client import HTTPClient


class CustomerAPI:
    CUSTOMER = '/customer/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.CUSTOMERS.value
        }

    def get_all_customers(self) -> tuple:
        path = self.CUSTOMER
        response = self.client.get(path, params=self.params)

        if response.status_code in range(200, 300):
            model = GetAllCustomersSuccessResponse(**response.json()) # Success model
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_customer(self, id: int) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.get(path, params=self.params)

        if response.status_code in range(200, 300):
            model = GetCustomerSuccessResponse(**response.json())  # Success model
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def create_customer(self, data: dict) -> tuple:
        path = self.CUSTOMER
        response = self.client.post(path, data=data, params=self.params)

        if response.status_code in range(200, 300):
            model = CreateCustomerSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_customer(self, id: int, data: dict) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.patch(path, data=data, params=self.params)

        if response.status_code in range(200, 300):
            model = UpdateCustomerSuccessResponse(**response.json())  # Success model
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_customer(self, id: int) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.delete(path, params=self.params)

        if response.status_code in range(200, 300):
            model = None  # Success response doesn't have body
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def send_request_without_section_param(self, method: str, id: int = None, **kwargs):
        # TODO: think about logic for tests without section
        path = f'{self.CUSTOMER}{id}' if id else self.CUSTOMER
        response = self.client.send_request(method, path, **kwargs)
        model = ErrorResponse(**response.json())

        return response, model
