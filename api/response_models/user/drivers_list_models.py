from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.response_models.response_models import SuccessResponse


"""
Get all drivers
"""


class _Driver(BaseModel):
    id: StrictInt
    first_name: constr(min_length=1, strict=True)
    last_name: constr(min_length=1, strict=True)
    email: constr(min_length=1, strict=True)
    phone_number: constr(min_length=1, strict=True)
    facility: Optional[StrictInt]


class _GetAllDriversDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_Driver]


class GetAllDriversSuccessResponse(SuccessResponse):
    data: _GetAllDriversDataField
