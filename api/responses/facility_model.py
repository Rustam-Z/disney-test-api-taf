from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr, validator

from api.responses.response_models import SuccessResponse


class _Facility(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)
    phone_number: constr(min_length=1, strict=True)
    timezone: constr(min_length=1, strict=True)
    status: constr(min_length=1, strict=True)
    country: constr(min_length=1, strict=True)
    state: constr(min_length=1, strict=True)
    city: constr(min_length=1, strict=True)
    address_line1: constr(min_length=1, strict=True)
    address_line2: Optional[StrictStr]
    zip_code: str
    customers: List[StrictInt]
    threshold: float
    warning_threshold: float
    critical_threshold: float


class _Customers(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _FacilityWithCustomers(_Facility):
    customers: List[_Customers]


"""
Get facility
"""


class GetFacilitySuccessResponse(SuccessResponse):
    data: _FacilityWithCustomers


"""
Get all facilities
"""


class _GetAllFacilitiesDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_FacilityWithCustomers]


class GetAllFacilitiesSuccessResponse(SuccessResponse):
    data: _GetAllFacilitiesDataField


"""
Create facility
"""


class CreateFacilitySuccessResponse(SuccessResponse):
    data: _Facility


"""
Update facility
"""


class UpdateFacilitySuccessResponse(SuccessResponse):
    data: _Facility
