from typing import List, Optional

from pydantic import BaseModel, constr, validator, StrictStr, StrictInt, StrictBool

from api.responses.response_models import SuccessResponse


"""
Menu list
"""


class _MenuListResultField(BaseModel):
    id: StrictInt
    title: constr(min_length=1)  # If an empty string is passed in, a validation error will be raised.
    route: constr(min_length=1)
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
    title: constr(min_length=1)
    route: constr(min_length=1)
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
