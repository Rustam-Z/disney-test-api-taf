from typing import Optional

from pydantic import BaseModel, StrictInt, constr

from api.responses.response_models import SuccessResponse


class _InventoryItemType(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)
    status: constr(min_length=1, strict=True)
    description: Optional[constr(min_length=1, strict=True)]
    category: StrictInt


"""
Create item type
"""


class CreateInventoryItemTypeSuccessResponse(SuccessResponse):
    data: _InventoryItemType
