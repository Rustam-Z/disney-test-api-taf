"""
Token and refresh token responses.
"""

from pydantic import BaseModel, StrictStr, StrictInt, StrictBool

from api.responses.response_models import SuccessResponse


class _TokenDataField(BaseModel):
    refresh: StrictStr
    access: StrictStr
    id: StrictInt
    is_superuser: StrictBool


class _RefreshTokenDataField(BaseModel):
    refresh: StrictStr
    access: StrictStr


class TokenSuccessResponse(SuccessResponse):
    data: _TokenDataField


class RefreshTokenSuccessResponse(SuccessResponse):
    data: _RefreshTokenDataField
