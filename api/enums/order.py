from enum import Enum


class OrderStatuses(Enum):
    READY_FOR_DELIVERY = "ready_for_delivery"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    ARRIVED_AT_FACILITY = "arrived_at_facility"
