from api.enums.params import Param
from api.enums.sections import Section
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse


class CartBuildAPI:
    CART_BUILD = '/metro/cart-build/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {  # Section query string param.
            Param.SECTION.value: Section.CUSTOMERS.value
        }

    def create_cart(self, data: dict, **kwargs):
        ...

    def get_cart(self, **kwargs):
        ...
