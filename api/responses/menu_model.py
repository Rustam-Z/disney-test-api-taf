from typing import List, Optional

from pydantic import BaseModel, validator, StrictStr, StrictInt, StrictBool

from api.responses.response_models import SuccessResponse


"""
Menu list
"""


class _MenuListResultField(BaseModel):
    id: StrictInt
    title: StrictStr
    route: StrictStr
    icon: Optional[str]
    order: StrictInt


class _MenuListDataField(BaseModel):
    results: List[_MenuListResultField]


class MenuListSuccessResponse(SuccessResponse):
    data: _MenuListDataField

    @validator('message')
    def check_message(cls, value):
        expected_message = 'Successfully'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value


"""
User menus
"""


class _UserMenusResultField(BaseModel):
    title: StrictStr
    route: StrictStr
    icon: Optional[str] = None
    order: StrictInt
    children: List
    edit: StrictBool
    view: StrictBool


class _UserMenusDataField(BaseModel):
    results: List[_UserMenusResultField]


class UserMenusSuccessResponse(SuccessResponse):
    data: _MenuListDataField

    @validator('message')
    def check_message(cls, value):
        expected_message = 'Successfully'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value
