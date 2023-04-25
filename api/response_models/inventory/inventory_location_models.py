from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.response_models.response_models import SuccessResponse


class _InventoryLocation(BaseModel):
    id: StrictInt
    facility: StrictInt
    name: constr(min_length=1, strict=True)
    description: constr(min_length=1, strict=True)
    reader_name: constr(min_length=1, strict=True)
    mac_address: constr(min_length=1, strict=True)
    antenna_port: constr(min_length=1, strict=True)
    type: constr(min_length=1, strict=True)


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)



class _InventoryLocationComplex(_InventoryLocation):
    facility: _FacilityField
    status: constr(min_length=1, strict=True)


"""
Get inventory location
"""


class GetInventoryLocationSuccessResponse(SuccessResponse):
    data: _InventoryLocationComplex


"""
Get all inventory locations
"""


class _GetAllInventoryLocationDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_InventoryLocationComplex]


class GetAllInventoryLocationSuccessResponse(SuccessResponse):
    data: _GetAllInventoryLocationDataField


"""
Create inventory location
"""


class CreateInventoryLocationSuccessResponse(SuccessResponse):
    data: _InventoryLocation


"""
Update inventory location
"""


class UpdateInventoryLocationSuccessResponse(SuccessResponse):
    data: _InventoryLocation
