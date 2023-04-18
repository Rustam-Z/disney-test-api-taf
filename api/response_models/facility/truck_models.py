from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.response_models.response_models import SuccessResponse


class _Truck(BaseModel):
    id: StrictInt
    facility: StrictInt
    number: constr(min_length=1, strict=True)
    bin_capacity: StrictInt
    weight_capacity: StrictInt
    status: constr(min_length=1, strict=True)


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _TruckComplex(_Truck):
    facility: _FacilityField


"""
Get orders
"""


class GetTruckSuccessResponse(SuccessResponse):
    data: _TruckComplex


"""
Create order
"""


class CreateTruckSuccessResponse(SuccessResponse):
    data: _Truck


"""
Update order
"""


class UpdateTruckSuccessResponse(SuccessResponse):
    data: _Truck
