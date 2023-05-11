from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.response_models.response_models import SuccessResponse


"""
Get orders
"""


class _Order(BaseModel):
    id: StrictInt
    customer_name: constr(min_length=1, strict=True)
    dropoff_date_end: datetime
    dropoff_date_start: datetime
    unique_id: constr(min_length=1, strict=True)


class _GetOrdersDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_Order]


class GetOrders(SuccessResponse):
    data: _GetOrdersDataField


"""
Get metros list
"""


class _ItemTypeQuantity(BaseModel):
    id: StrictInt
    item_type: StrictInt
    quantity: StrictInt
    item_type_name: constr(min_length=1, strict=True)


class _MetroConfig(BaseModel):
    id: StrictInt
    description: constr(min_length=1, strict=True)
    item_type_quantities: List[_ItemTypeQuantity]


class _Metro(BaseModel):
    cart_build_id: StrictInt
    metro_qr_code: constr(min_length=1, strict=True)
    metro_config: _MetroConfig


class _GetMetroDataField(BaseModel):
    results: List[_Metro]


class GetMetroList(SuccessResponse):
    data: _GetMetroDataField
