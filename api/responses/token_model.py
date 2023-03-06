"""
Usage:
    data_ = {"status": False, "message": "Error", "data": None,
             "error": {"detail": "No active account found with the given credentials"}}
    model_ = TokenErrorResponse(**data_)

"""
from typing import Dict

from pydantic import BaseModel, validator, StrictStr, StrictInt, StrictBool

from api.responses.response_model import SuccessResponse, ErrorResponse


"""
Token
"""


class _TokenDataField(BaseModel):
    refresh: StrictStr
    access: StrictStr
    id: StrictInt
    is_superuser: StrictBool


class TokenSuccessResponse(SuccessResponse):
    data: _TokenDataField

    @validator('message')
    def check_message(cls, value):
        expected_message = 'Successfully'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value


class TokenErrorResponse(ErrorResponse):
    error: Dict

    @validator('message')
    def check_message(cls, value):
        expected_message = 'Error'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value


"""
Refresh token

Error response is the same for Token and Refresh token.
"""


class _RefreshTokenDataField(BaseModel):
    refresh: StrictStr
    access: StrictStr


class RefreshTokenSuccessResponse(SuccessResponse):
    data: _RefreshTokenDataField

    @validator('message')
    def check_message(cls, value):
        expected_message = 'Successfully'
        if value != expected_message:
            raise ValueError(f'message must be "{expected_message}"')
        return value
