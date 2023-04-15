from typing import List, Optional

from pydantic import BaseModel, constr, StrictInt, StrictBool

from api.response_models.response_models import SuccessResponse


"""
Menu list
"""


class _MenuListResultField(BaseModel):
    id: StrictInt
    title: constr(min_length=1, strict=True)  # If an empty string is passed in, a validation error will be raised.
    route: constr(min_length=1, strict=True)
    icon: Optional[str]
    order: StrictInt


class _MenuListDataField(BaseModel):
    results: List[_MenuListResultField]


class MenuListSuccessResponse(SuccessResponse):
    data: _MenuListDataField


"""
User menus
"""


class _UserMenusResultField(BaseModel):
    title: constr(min_length=1, strict=True)
    route: constr(min_length=1, strict=True)
    icon: Optional[str] = None
    order: StrictInt
    children: List
    edit: StrictBool
    view: StrictBool


class _UserMenusDataField(BaseModel):
    results: List[_UserMenusResultField]


class UserMenusSuccessResponse(SuccessResponse):
    data: _UserMenusDataField
