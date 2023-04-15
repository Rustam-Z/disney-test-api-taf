from typing import Optional

from pydantic import BaseModel, StrictInt, constr, StrictFloat

from api.responses.response_models import SuccessResponse


class _FacilityItemType(BaseModel):
    # TODO: check the types
    id: StrictInt
    facility: Optional[StrictInt]
    item_type: StrictInt
    name: constr(min_length=1, strict=True)
    weight: StrictFloat
    ideal_par_level: Optional[float] = None
    cost: Optional[float] = None
    status: constr(min_length=1, strict=True)
    manufacturer: Optional[str] = None
    supplier: Optional[str] = None
    supplier_product_name: Optional[str] = None
    sku: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    care_instructions: Optional[str] = None
    life_span: Optional[int] = None


"""
Create item type
"""


class CreateFacilityItemTypeSuccessResponse(SuccessResponse):
    data: _FacilityItemType
