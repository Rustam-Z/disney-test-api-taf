from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr, StrictBool

from api.responses.response_models import SuccessResponse


class _Role(BaseModel):
    id: StrictInt
    facility: Optional[StrictInt]
    name: constr(min_length=1, strict=True)
    description: constr(min_length=1, strict=True)
    is_driver: StrictBool


class _Facility(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _SectionPermissionSection(BaseModel):
    id: StrictInt
    title: constr(min_length=1, strict=True)
    route: constr(min_length=1, strict=True)
    icon: Optional[str] = None
    order: StrictInt


class _SectionPermission(BaseModel):
    id: StrictInt
    section: _SectionPermissionSection
    is_editable: StrictBool
    is_viewable: StrictBool


class _RolesWithSections(BaseModel):
    id: StrictInt
    facility: Optional[_Facility]
    name: constr(min_length=1, strict=True)
    is_driver: StrictBool
    section_permissions: List[_SectionPermission]
    description: Optional[constr(min_length=1, strict=True)]


"""
Get role
"""


class GetRoleSuccessResponse(SuccessResponse):
    data: _RolesWithSections


"""
Get all roles
"""


class _GetAllRolesDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_RolesWithSections]


class GetAllRolesSuccessResponse(SuccessResponse):
    data: _GetAllRolesDataField


"""
Create role
"""


class CreateRoleSuccessResponse(SuccessResponse):
    data: _Role


"""
Update role
"""


class UpdateRoleSuccessResponse(SuccessResponse):
    data: _Role
