from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.response_models.response_models import SuccessResponse


class _Order(BaseModel):
    id: StrictInt
    unique_id: constr(min_length=1, strict=True)
    disney_id: Optional[StrictStr]
    facility: StrictInt
    customer: StrictInt
    status: constr(min_length=1, strict=True)
    dropoff_date_start: constr(min_length=1, strict=True)
    dropoff_date_end: constr(min_length=1, strict=True)
    actual_dropoff_date: Optional[StrictStr]
    note: Optional[StrictStr]
    driver_note: Optional[StrictStr]
    dropoff_at_customer_note: Optional[StrictStr]


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _CustomerField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _OrderComplex(_Order):
    facility: _FacilityField
    customer: _CustomerField
    out_for_delivery_date: Optional[StrictStr]
    dropoff_metros_count: StrictInt
    created_at: constr(min_length=1, strict=True)


"""
Get order
"""


class GetOrderSuccessResponse(SuccessResponse):
    data: _OrderComplex


"""
Get all orders
"""


class _GetAllOrdersDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_OrderComplex]


class GetAllOrderSuccessResponse(SuccessResponse):
    data: _GetAllOrdersDataField


"""
Create order
"""


class CreateOrderSuccessResponse(SuccessResponse):
    data: _Order


"""
Update delivery schedule
"""


class UpdateOrderSuccessResponse(SuccessResponse):
    data: _Order
