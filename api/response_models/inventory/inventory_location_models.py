from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.response_models.response_models import SuccessResponse


class _InventoryLocation(BaseModel):
    id: StrictInt
    facility: StrictInt
    name: constr(min_length=1, strict=True)
    description: constr(min_length=1, strict=True)
    reader_name: constr(min_length=1, strict=True)
    mac_address: constr(min_length=1, strict=True)
    antenna_port: constr(min_length=1, strict=True)
    type: constr(min_length=1, strict=True)

class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)



class _InventoryLocationComplex(_InventoryLocation):
    facility: _FacilityField
    status: constr(min_length=1, strict=True)


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


class GetAllOrdersSuccessResponse(SuccessResponse):
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
