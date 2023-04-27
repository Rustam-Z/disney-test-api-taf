from api.enums.params import Param
from api.enums.sections import Section
from api.response_models.response_models import ErrorResponse
from core.http_client import HTTPClient
from api.response_models.customer.customer_contact_models import (
    GetCustomerContactSuccessResponse,
    CreateCustomerContactSuccessResponse,
    GetAllCustomerContactsSuccessResponse,
    UpdateCustomerContactSuccessResponse,
)


class CustomerContactAPI:
    CUSTOMER_CONTACT = '/customer/contact/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.CUSTOMER_CONTACT.value
        }

    def get_all_customer_contacts(self, **kwargs) -> tuple:
        path = self.CUSTOMER_CONTACT
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetAllCustomerContactsSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def get_customer_contact(self, id: int, **kwargs) -> tuple:
        path = f'{self.CUSTOMER_CONTACT}{id}'
        response = self.client.get(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = GetCustomerContactSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def create_customer_contact(self, data: dict, **kwargs) -> tuple:
        path = self.CUSTOMER_CONTACT
        response = self.client.post(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 201:
            response_payload = CreateCustomerContactSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def update_customer_contact(self, id: int, data: dict, **kwargs) -> tuple:
        path = f'{self.CUSTOMER_CONTACT}{id}'
        response = self.client.patch(path, json=data, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code == 200:
            response_payload = UpdateCustomerContactSuccessResponse(**response.json())
        elif response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload

    def delete_customer_contact(self, id: int, **kwargs) -> tuple:
        path = f'{self.CUSTOMER_CONTACT}{id}'
        response = self.client.delete(path, params=self.params, **kwargs)
        response_payload = response.content

        if response.status_code in range(400, 500):
            response_payload = ErrorResponse(**response.json())

        return response, response_payload
