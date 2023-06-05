from typing import List, Optional, Union

from pydantic import BaseModel, StrictInt, constr, StrictStr, StrictBool

from api.response_models.response_models import SuccessResponse


class _User(BaseModel):
    id: StrictInt
    facility: Optional[StrictInt]
    first_name: constr(min_length=1, strict=True)
    last_name: constr(min_length=1, strict=True)
    title: constr(min_length=1, strict=True)
    role: Union[StrictInt, None]
    email: constr(min_length=1, strict=True)
    phone_number: constr(min_length=1, strict=True)
    is_staff: StrictBool
    is_active: StrictBool
    is_superuser: StrictBool
    created_by: Optional[dict]
    updated_by: Optional[dict]
    has_daily_report_access: StrictBool
    has_weekly_report_access: StrictBool
    has_monthly_report_access: StrictBool
    groups: Optional[list]
    user_permissions: Optional[list]


class _RoleField(BaseModel):
    id: StrictInt
    role_name: constr(min_length=1, strict=True)


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _UserWithRoleAndFacilityInfo(BaseModel):
    id: StrictInt
    facility: Optional[_FacilityField]
    first_name: constr(min_length=1, strict=True)
    last_name: constr(min_length=1, strict=True)
    title: constr(min_length=1, strict=True)
    role: Optional[_RoleField]
    email: constr(min_length=1, strict=True)
    phone_number: constr(min_length=1, strict=True)


"""
Get user
"""


class GetUserSuccessResponse(SuccessResponse):
    data: _UserWithRoleAndFacilityInfo


"""
Get all users
"""


class _GetAllUsersDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_UserWithRoleAndFacilityInfo]


class GetAllUsersSuccessResponse(SuccessResponse):
    data: _GetAllUsersDataField


"""
Create user
"""


class CreateUserSuccessResponse(SuccessResponse):
    data: _User


"""
Update user
"""


class UpdateUserSuccessResponse(SuccessResponse):
    data: _User
