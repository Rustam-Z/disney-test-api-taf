from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr, StrictFloat

from api.response_models.response_models import SuccessResponse


class _Truck(BaseModel):
    id: StrictInt
    facility: StrictInt
    number: constr(min_length=1, strict=True)
    bin_capacity: StrictInt
    weight_capacity: StrictFloat
    status: constr(min_length=1, strict=True)


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _TruckComplex(_Truck):
    facility: _FacilityField


"""
Get truck
"""


class GetTruckSuccessResponse(SuccessResponse):
    data: _TruckComplex


"""
Get all trucks
"""
class _GetAllTrucksDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_TruckComplex]


class GetAllTrucksSuccessResponse(SuccessResponse):
    data: _GetAllTrucksDataField


"""
Create truck
"""


class CreateTruckSuccessResponse(SuccessResponse):
    data: _Truck


"""
Update truck
"""


class UpdateTruckSuccessResponse(SuccessResponse):
    data: _Truck
