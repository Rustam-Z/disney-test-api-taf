from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, StrictInt, constr, StrictStr, EmailStr

from api.response_models.response_models import SuccessResponse


"""
Get all metros
"""


class _CreateUpdatedByField(BaseModel):
    id: StrictInt
    email: EmailStr


class _ResultsField(BaseModel):
    id: StrictInt
    facility_name: constr(min_length=1, strict=True)
    metro_qr_code: constr(min_length=1, strict=True)
    metro_epc: constr(min_length=1, strict=True)
    metro_human_readable: constr(min_length=1, strict=True)
    created_by: _CreateUpdatedByField
    updated_by: _CreateUpdatedByField
    created_at: datetime


class _GetAllMetrosDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_ResultsField]


class GetAllMetrosSuccessResponse(SuccessResponse):
    data: _GetAllMetrosDataField


"""
Create metro
"""


class _CreateMetroDataField(BaseModel):
    id: StrictInt
    facility: StrictInt


class CreateMetroResponse(SuccessResponse):
    data: _CreateMetroDataField
