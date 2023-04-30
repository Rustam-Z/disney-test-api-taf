"""
Possible section values in section param.
"""

from enum import Enum


class Section(Enum):
    """
    Check /user/menu-list/ endpoint response data.
    The values should match.
    """
    CUSTOMERS = 'customers'
    FACILITY = 'facility'
    ROLES = 'roles'
    USERS = 'users'
    INVENTORY_CATEGORY = 'inventory-category'
    INVENTORY_ITEM_TYPE = 'inventory-item-type'
    FACILITY_ITEM_TYPE = 'facility-item-type'
    METRO = 'metro'
    METRO_COMMISSION = 'metro-commission'
    METRO_ITEM_CONFIGURATION = 'metro-item-configuration'
    DELIVERY_SCHEDULE = 'delivery-schedule'
    ORDER = 'orders'
    TRUCK = 'trucks'
    INVENTORY_LOCATION = 'inventory-location'
    CUSTOMER_CONTACT = 'customer-contact'
    DRIVER_ASSIGNMENT = 'driver-assignment'
