import random
from datetime import datetime, timedelta
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

    def role(
        self,
        sections: List,
        permissions: dict = None,
        facility_id: int = None,
        is_driver: bool = False,
        **kwargs
    ) -> dict:
        """
        menu_list: the ids of menu lists to give permission. It is a menu list results model.
        permissions: section_id: [is_editable, is_viewable]
        facility_id:
            if None and superuser makes request then it is not assigned to facility.
            if facility user makes request, then it is automatically assigned to facility.
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

    def user(self, role_id: int = None, facility_id: int = None, **kwargs) -> dict:
        data = {
            "facility": facility_id,
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "title": self.fake.name(),
            "role": role_id,
            "email": self.fake.email(),
            "phone_number": self.fake.custom_phone_number(),
            "password": self.fake.password(),
        }
        data.update(kwargs)
        return data

    def inventory_category(self, **kwargs) -> dict:
        data = {
            "name": self.fake.name(),
        }
        data.update(kwargs)
        return data

    def inventory_item_type(self, category_id: int = None, **kwargs) -> dict:
        data = {
            "name": self.fake.name(),
            "description": self.fake.text(),
            "category": category_id,
        }
        data.update(kwargs)
        return data

    def facility_item_type(self, item_type_id: int = None, facility_id: int = None, **kwargs) -> dict:
        data = {
            "facility": facility_id,
            "item_type": item_type_id,  # Inventory item type id
            "name": self.fake.name(),
            "weight": self.fake.pyint(),
        }
        data.update(kwargs)
        return data

    def metro(
        self,
        facility_id: int = None,
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
            "process_status": process_status,
        }
        data.update(kwargs)
        return data

    def metro_for_commission(self, facility_id: int = None, **kwargs) -> dict:
        """
        This model is used in metro commission.
        """
        data = {
            "facility": facility_id,
            "qr_code": self.fake.ean(),
            "rfid_tag_id": self.fake.ean(),
            "human_readable": self.fake.name(),
        }
        data.update(kwargs)
        return data

    def metro_item_configuration(
        self,
        facility_id: int = None,
        facility_item_type_ids: list[int] = None,
        **kwargs
    ) -> dict:
        item_type_quantities = []

        if facility_item_type_ids is not None:
            for id_ in facility_item_type_ids:
                item_type_quantities.append({
                    "item_type": id_,
                    "quantity": self.fake.pyint()
                })

        data = {
            "facility": facility_id,
            "item_type_quantities": item_type_quantities,  # Facility item type.
            "qr_code": self.fake.ean(),
            "description": self.fake.text(),
        }

        data.update(kwargs)
        return data

    def cart(self, metro_qr_code: str = None, metro_config_qr_code: str = None, **kwargs) -> dict:
        data = {
            "metro_qr_code": metro_qr_code,
            "metro_config_qr_code": metro_config_qr_code,
        }
        data.update(kwargs)
        return data

    def delivery_schedule(self, facility_id: int = None, customer_id: int = None, **kwargs) -> dict:
        data = {
            "facility": facility_id,
            "customer": customer_id,
            "days": ["0", "1"],
            "start_time": "08:00:00",
            "end_time": "10:00:00",
        }
        data.update(kwargs)
        return data

    def order(self, facility_id: int = None, customer_id: int = None, **kwargs) -> dict:
        """
        Creates fake order, with the start date == tomorrow.
        """
        now_utc = datetime.now()
        tomorrow_utc = now_utc + timedelta(days=1)
        future_utc = now_utc + timedelta(days=random.randint(2, 10))

        tomorrow_date_str = tomorrow_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        future_date_str = future_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = {
            "facility": facility_id,
            "customer": customer_id,
            "dropoff_date_start": tomorrow_date_str,
            "dropoff_date_end": future_date_str,
        }

        data.update(kwargs)
        return data

    def truck(self, facility_id: int = None, **kwargs) -> dict:
        data = {
            "facility": facility_id,
            "number": random.randint(1000, 10000),
            "bin_capacity": random.randint(50, 300),
            "weight_capacity": random.randint(50, 500),
        }
        data.update(kwargs)
        return data

    def inventory_location(self, facility_id: int = None, **kwargs) -> dict:
        name = self.fake.name()
        address = f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        antenna = random.randint(0, 7)
        data = {
            "name": name,
            "facility": facility_id,
            "description": name,
            "reader_name": name,
            "mac_address": address,
            "antenna_port": f"{antenna},{antenna+1},{antenna+2}",
            "type": "exit",
        }
        data.update(kwargs)
        return data

    def customer_contact(self, facility_id: int = None, customer_id: int = None, **kwargs) -> dict:
        data = {
            "facility": facility_id,
            "customer": customer_id,
            "name": self.fake.name(),
            "email": self.fake.email(),
            "phone_number": f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            "title": self.fake.name(),
            "has_dropoff_access": bool(random.randint(0, 1)),
            "has_invoice_access": bool(random.randint(0, 1)),
        }
        data.update(kwargs)
        return data

    def driver_assignment_to_one_order(
        self,
        truck: int = None,
        drivers: list[int] = None,
        assigned_orders: list[int] = None,
        unassigned_orders: list[int] = None,
    ) -> list:
        data = [{
            "truck": truck,
            "drivers": drivers,
            "assigned_orders": [{'order_id': order_id} for order_id in assigned_orders],
            "unassigned_orders": [{'order_id': order_id} for order_id in unassigned_orders],
        }]
        return data
