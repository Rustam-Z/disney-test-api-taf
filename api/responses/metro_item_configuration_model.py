from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.responses.response_models import SuccessResponse


class _ItemTypeQuantityField(BaseModel):
    id: StrictInt
    item_type: StrictInt
    quantity: StrictInt
    item_type_name: constr(min_length=1, strict=True)


class _ConfigField(BaseModel):
    id: StrictInt
    facility: StrictInt
    qr_code: constr(min_length=1, strict=True)
    description: constr(min_length=1, strict=True)
    goal: StrictInt
    item_type_quantities: List[_ItemTypeQuantityField]


"""
Get all configs
"""


class _ResultsField(BaseModel):
    id: StrictInt
    facility_name: constr(min_length=1, strict=True)
    qr_code: constr(min_length=1, strict=True)
    goal: StrictInt
    description: constr(min_length=1, strict=True)
    status: constr(min_length=1, strict=True)


class _GetAllConfigsDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_ResultsField]


class GetAllConfigsSuccessResponse(SuccessResponse):
    data: _GetAllConfigsDataField


"""
Get config
"""


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _GetConfigField(_ConfigField):
    facility: _FacilityField
    status: constr(min_length=1, strict=True)


class GetConfigSuccessResponse(SuccessResponse):
    data: _GetConfigField


"""
Create config
"""


class CreateConfigSuccessResponse(SuccessResponse):
    data: _ConfigField


"""
Update config
"""


class UpdateConfigSuccessResponse(SuccessResponse):
    data: _ConfigField
