from enum import Enum


class ErrorDetail(Enum):
    TOKEN_IS_INVALID = 'Token is invalid or expired.'
    FIELD_MAY_NOT_BE_BLANK = 'This field may not be blank.'
    WRONG_CREDENTIALS = 'No active account found with the given credentials'
