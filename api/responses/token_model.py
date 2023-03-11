"""
Token and refresh token responses.
"""

from pydantic import BaseModel, StrictInt, StrictBool, constr

from api.responses.response_models import SuccessResponse


class _TokenDataField(BaseModel):
    refresh: constr(min_length=1, strict=True)
    access: constr(min_length=1, strict=True)
    id: StrictInt
    is_superuser: StrictBool


class _RefreshTokenDataField(BaseModel):
    refresh: constr(min_length=1, strict=True)
    access: constr(min_length=1, strict=True)


class TokenSuccessResponse(SuccessResponse):
    data: _TokenDataField


class RefreshTokenSuccessResponse(SuccessResponse):
    data: _RefreshTokenDataField
