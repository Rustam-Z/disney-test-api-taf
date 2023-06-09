from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr, StrictBool

from api.response_models.response_models import SuccessResponse


class _CustomerContact(BaseModel):
    id: StrictInt
    facility: StrictInt
    customer: StrictInt
    name: constr(min_length=1, strict=True)
    email: constr(min_length=1, strict=True)
    phone_number: constr(min_length=1, strict=True)
    title: constr(min_length=1, strict=True)
    has_dropoff_access: StrictBool
    has_invoice_access: StrictBool


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _CustomerField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _CustomerContactComplex(_CustomerContact):
    facility: _FacilityField
    customer: _CustomerField


"""
Get customer contact
"""


class GetCustomerContactSuccessResponse(SuccessResponse):
    data: _CustomerContactComplex


"""
Get all customer contacts
"""


class _GetAllCustomerContactsDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_CustomerContactComplex]


class GetAllCustomerContactsSuccessResponse(SuccessResponse):
    data: _GetAllCustomerContactsDataField


"""
Create customer contact
"""


class CreateCustomerContactSuccessResponse(SuccessResponse):
    data: _CustomerContact


"""
Update customer contact
"""


class UpdateCustomerContactSuccessResponse(SuccessResponse):
    data: _CustomerContact
