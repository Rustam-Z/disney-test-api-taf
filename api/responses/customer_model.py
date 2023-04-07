from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.responses.response_models import SuccessResponse


class _Customer(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)
    barcode: constr(min_length=1, strict=True)
    address_line1: constr(min_length=1, strict=True)
    address_line2: Optional[StrictStr]
    replenishment_threshold: Optional[float]
    city: constr(min_length=1, strict=True)
    state: constr(min_length=1, strict=True)
    country: constr(min_length=1, strict=True)
    zip_code: Optional[StrictStr]
    status: constr(min_length=1, strict=True)
    main_phone_number: constr(min_length=1, strict=True)
    brand: Optional[StrictStr]
    hotel_ownership: List[StrictInt] = []


"""
Get customer
"""


class GetCustomerSuccessResponse(SuccessResponse):
    data: _Customer


"""
Update customer
"""


class UpdateCustomerSuccessResponse(SuccessResponse):
    data: _Customer


"""
Get all customers
"""


class _GetAllCustomersDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_Customer]


class GetAllCustomersSuccessResponse(SuccessResponse):
    data: _GetAllCustomersDataField


"""
Create customer
"""


class _CreateCustomerDataField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)
    barcode: constr(min_length=1, strict=True)
    timezone: constr(min_length=1, strict=True)
    address_line1: constr(min_length=1, strict=True)
    address_line2: Optional[StrictStr]
    par_level: Optional[StrictInt] = None
    replenishment_threshold: Optional[StrictInt] = None
    city: constr(min_length=1, strict=True)
    state: constr(min_length=1, strict=True)
    country: constr(min_length=1, strict=True)
    zip_code: constr(min_length=1, strict=True)
    main_phone_number: constr(min_length=1, strict=True)
    brand: Optional[constr(min_length=1, strict=True)] = None
    hotel_ownership: List


class CreateCustomerSuccessResponse(SuccessResponse):
    data: _CreateCustomerDataField
