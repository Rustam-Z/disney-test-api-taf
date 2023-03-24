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
