import random
from typing import List

from api.enums.metro import MetroLaundryStatuses, MetroProcessStatuses
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

        data.update(kwargs)  # Update data with kwargs values
        return data

    def facility(self, customers: List[int] = None, **kwargs) -> dict:
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
            "customers": customers,
            "threshold": self.fake.pyint(),
            "warning_threshold": self.fake.pyint(),
            "critical_threshold": self.fake.pyint(),
        }

        data.update(kwargs)
        return data

    def role(self,
             sections: List,
             permissions: dict = None,
             facility_id: int = None,
             is_driver: bool = False,
             **kwargs
             ) -> dict:
        """
        menu_list: the ids of menu lists to give permission. It is a menu list results model.
        permissions: section_id: [is_editable, is_viewable]
        facility_id: if None then it is not assigned to facility.

        """
        if permissions is None:
            permissions = {}

        section_permissions = []
        section_ids: List[int] = [section.id for section in sections]
        for section_id in section_ids:
            section_permissions.append(
                {
                    'section': section_id,
                    'is_editable': permissions.get(section_id)[0] if permissions.get(section_id) else True,
                    'is_viewable': permissions.get(section_id)[1] if permissions.get(section_id) else True,
                }
            )

        data = {
            'name': self.fake.name(),
            'description': self.fake.text(),
            'is_driver': is_driver,
            'facility': facility_id,
            'section_permissions': section_permissions,
        }

        data.update(kwargs)
        return data

    def user(self, role_id: int, facility_id: int = None, **kwargs) -> dict:
        data = {
            "facility": facility_id,
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "title": self.fake.name(),
            "role": role_id,
            "email": self.fake.email(),
            "phone_number": self.fake.custom_phone_number(),
            "password": self.fake.password()
        }

        data.update(kwargs)
        return data

    def inventory_category(self, **kwargs) -> dict:
        data = {
            "name": self.fake.name()
        }

        data.update(kwargs)
        return data

    def inventory_item_type(self, category_id: int, **kwargs) -> dict:
        data = {
            "name": self.fake.name(),
            "description": self.fake.text(),
            "category": category_id
        }

        data.update(kwargs)
        return data

    def facility_item_type(self, item_type_id: int, facility_id: int = None, **kwargs) -> dict:
        data = {
            "facility": facility_id,
            "item_type": item_type_id,  # Inventory item type id
            "name": self.fake.name(),
            "weight": self.fake.pyint()
        }

        data.update(kwargs)
        return data

    def metro(
            self,
            facility_id: int,
            laundry_status: str = MetroLaundryStatuses.NONE.value,
            process_status: str = MetroProcessStatuses.STAGED_IN_INVENTORY.value,
            **kwargs
    ) -> dict:
        """
        MetroLaundryStatuses
            clean
            soiled
            none


        MetroProcessStatuses
            staged_in_inventory
            ready_for_delivery
            out_for_delivery
            delivered
            arrived_at_facility
            ready_for_cart_build

        NOTE! Check https://github.com/Laundris/disney-backend/blob/dev/metro/enums.py for status updates.

        """
        data = {
            "facility": facility_id,
            "human_readable": self.fake.name(),
            "qr_code": self.fake.ean(),
            "rfid_tag_id": self.fake.ean(),
            "laundry_status": laundry_status,
            "process_status": process_status
        }

        data.update(kwargs)
        return data