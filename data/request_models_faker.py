import random
from typing import List

from data.custom_faker import CustomFaker


class RequestModelsFaker:
    def __init__(self):
        self.fake = CustomFaker()

    def customer(self, **kwargs) -> dict:
        """
        Args:
            **kwargs: The values that need to be overridden in the data dictionary.

        Returns: Dict, fake request model.

        """
        data = {
            'name': self.fake.name(),
            'barcode': self.fake.ean13(),
            'address_line1': self.fake.address(),
            'address_line2': self.fake.address(),
            'city': self.fake.city(),
            'state': self.fake.state(),
            'country': self.fake.country(),
            'zip_code': self.fake.zipcode(),
            'main_phone_number': self.fake.custom_phone_number(),
        }

        data.update(kwargs)   # Update data with kwargs values
        return data

    def facility(self, customers=None, **kwargs) -> dict:
        if customers is None:
            customers = []

        data = {
            "name": self.fake.name(),
            "phone_number": self.fake.custom_phone_number(),
            "turnaround_time": random.choice([48, 72]),
            "country": self.fake.country(),
            "state": self.fake.state(),
            "city": self.fake.city(),
            "address_line1": self.fake.address(),
            "address_line2": self.fake.address(),
            "zip_code": self.fake.zipcode(),
            "customers": customers
        }

        data.update(kwargs)
        return data
