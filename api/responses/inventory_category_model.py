from pydantic import BaseModel, StrictInt, constr

from api.responses.response_models import SuccessResponse


class _UserField(BaseModel):
    id: StrictInt
    email: constr(min_length=1, strict=True)


class _InventoryCategory(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)
    status: constr(min_length=1, strict=True)
    created_by: _UserField
    updated_by: _UserField


"""
Create category
"""


class CreateInventoryCategorySuccessResponse(SuccessResponse):
    data: _InventoryCategory
