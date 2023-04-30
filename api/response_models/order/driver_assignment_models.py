from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictFloat

from api.response_models.response_models import SuccessResponse


"""
Get truck orders and drivers
"""


class _TruckOrdersAndDrivers(BaseModel):
    id: StrictInt
    number: constr(min_length=1, strict=True)
    bin_capacity: StrictInt
    weight_capacity: StrictFloat
    drivers: Optional[List[StrictInt]]
    orders: List[StrictInt] = []


class GetTruckOrdersAndDrivers(SuccessResponse):
    data: List[_TruckOrdersAndDrivers]


"""
Get unassigned orders
"""


class _Order(BaseModel):
    customer_name: constr(min_length=1, strict=True)
    id: StrictInt
    scheduled_for_date_end: datetime
    scheduled_for_date_start: datetime
    scheduled_for_date_start: datetime


class _GetUnassignedOrdersDataField(BaseModel):
    results: List[_Order]


class GetUnassignedOrders(SuccessResponse):
    data: _GetUnassignedOrdersDataField


"""
Assign drivers and orders
"""


class AssignDriversAndOrders(SuccessResponse):
    ...
