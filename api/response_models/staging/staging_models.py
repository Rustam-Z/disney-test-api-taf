from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.response_models.response_models import SuccessResponse


class _Order(BaseModel):
    id: StrictInt
    customer_name: constr(min_length=1, strict=True)
    dropoff_date_end: datetime
    dropoff_date_start: datetime
    unique_id: constr(min_length=1, strict=True)


"""
Get orders
"""


class _GetOrdersDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_Order]


class GetOrders(SuccessResponse):
    data: _GetOrdersDataField
