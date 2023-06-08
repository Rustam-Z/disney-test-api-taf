from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, StrictInt, StrictBool, constr, StrictStr

from api.response_models.response_models import SuccessResponse


class _MetroField(BaseModel):
    id: StrictInt
    qr_code: constr(min_length=1, strict=True)
    human_readable: constr(min_length=1, strict=True)
    rfid_tag_id: constr(min_length=1, strict=True)


class _MetroConfigField(BaseModel):
    id: StrictInt
    qr_code: constr(min_length=1, strict=True)


class _Cart(BaseModel):
    id: StrictInt
    created_at: datetime
    updated_at: datetime
    metro: _MetroField
    metro_config: _MetroConfigField


"""
Create cart.
"""


class _CreateCartDataField(_Cart):
    is_rebuild: StrictBool


class CreateCartSuccessResponse(SuccessResponse):
    data: _CreateCartDataField


"""
Get cart model.
"""


class _GetCartDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_Cart]


class GetCartSuccessResponse(SuccessResponse):
    data: _GetCartDataField
