from enum import Enum


class MetroLaundryStatuses(Enum):
    CLEAN = "clean"
    SOILED = "soiled"
    NONE = "none"


class MetroProcessStatuses(Enum):
    STAGED_IN_INVENTORY = "staged_in_inventory"
    READY_FOR_DELIVERY = "ready_for_delivery"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    ARRIVED_AT_FACILITY = "arrived_at_facility"
    READY_FOR_CART_BUILD = "ready_for_cart_build"
