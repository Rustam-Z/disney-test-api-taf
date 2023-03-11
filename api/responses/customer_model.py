from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr

from api.responses.response_models import SuccessResponse


"""
Get all customers
"""


class _CreateCustomerDataField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)
    barcode: constr(min_length=1, strict=True)
    timezone: constr(min_length=1, strict=True)
    address_line1: constr(min_length=1, strict=True)
    address_line2: constr(min_length=1, strict=True)
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
