from enum import Enum


class ErrorDetail(Enum):
    TOKEN_IS_INVALID = 'Token is invalid or expired'
    FIELD_MAY_NOT_BE_BLANK = 'This field may not be blank.'
    WRONG_CREDENTIALS = 'No active account found with the given credentials'
    AUTH_CREDS_NOT_PROVIDED = 'Authentication credentials were not provided.'
    ONLY_SUPERUSER = 'Only Superuser can perform this action!'
    NO_PERMISSION = 'You do not have permission to perform this action.'
    NO_SUCH_MENU = 'There is no such menu route available.'
    NOT_FOUND = 'Not found.'
