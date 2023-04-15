from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.customer_model import (CreateCustomerSuccessResponse,
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

        if response.status_code in range(200, 300):
            model = GetAllCustomersSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def get_customer(self, id: int, **kwargs) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.get(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = GetCustomerSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def create_customer(self, data: dict, **kwargs) -> tuple:
        path = self.CUSTOMER
        response = self.client.post(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = CreateCustomerSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def update_customer(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = UpdateCustomerSuccessResponse(**response.json())
        else:
            model = ErrorResponse(**response.json())

        return response, model

    def delete_customer(self, id: int, **kwargs) -> tuple:
        path = f'{self.CUSTOMER}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)

        if response.status_code in range(200, 300):
            model = None  # Success response doesn't have body
        else:
            model = ErrorResponse(**response.json())

        return response, model
