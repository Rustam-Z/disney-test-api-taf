from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictFloat, validator

from api.response_models.response_models import SuccessResponse


class _Order(BaseModel):
    id: StrictInt
    customer_name: constr(min_length=1, strict=True)
    scheduled_for_date_end: datetime
    scheduled_for_date_start: datetime
    unique_id: constr(min_length=1, strict=True)


class _Driver(BaseModel):
    id: StrictInt
    facility: Optional[StrictInt]
    first_name: constr(min_length=1, strict=True)
    last_name: constr(min_length=1, strict=True)
    email: constr(min_length=1, strict=True)
    phone_number: constr(min_length=1, strict=True)


"""
Get truck orders and drivers
"""


class _TruckOrdersAndDrivers(BaseModel):
    id: StrictInt
    number: constr(min_length=1, strict=True)
    bin_capacity: StrictInt
    weight_capacity: StrictFloat
    drivers: Optional[List[_Driver]]
    orders: List[_Order] = []


class GetTruckOrdersAndDrivers(SuccessResponse):
    data: List[_TruckOrdersAndDrivers]


"""
Get unassigned orders
"""


class _GetUnassignedOrdersDataField(BaseModel):
    results: List[_Order]


class GetUnassignedOrders(SuccessResponse):
    data: _GetUnassignedOrdersDataField


"""
Assign drivers and orders
"""


class _AssignOrdersToTruckAndDriversDataField(BaseModel):
    message: constr(min_length=1, strict=True)

    @validator('message')
    def check_message(cls, value):
        expected_message = 'Drivers and Orders assignment process is Done!'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value


class AssignOrdersToTruckAndDrivers(SuccessResponse):
    data: _AssignOrdersToTruckAndDriversDataField
