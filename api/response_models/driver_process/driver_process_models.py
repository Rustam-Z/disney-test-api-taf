from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr, StrictBool

from api.response_models.response_models import SuccessResponse


"""
Get orders
"""


class _Customer(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _GetOrdersResultField(BaseModel):
    id: StrictInt
    disney_id: constr(min_length=1, strict=True)
    customer: _Customer
    dropoff_date_start: datetime
    dropoff_date_end: datetime
    is_fulfilled: StrictBool


class _GetOrdersDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_GetOrdersResultField]


class GetOrders(SuccessResponse):
    data: _GetOrdersDataField


"""
Get metro list
"""


class _GetMetroListResult(BaseModel):
    id: StrictInt
    human_readable: constr(min_length=1, strict=True)
    qr_code: constr(min_length=1, strict=True)
    rfid_tag_id: constr(min_length=1, strict=True)
    is_scanned: StrictBool
    metro_config_description: constr(min_length=1, strict=True)


class _GetMetroListDataField(BaseModel):
    results: List[_GetMetroListResult]


class GetMetroList(SuccessResponse):
    data: _GetMetroListDataField
