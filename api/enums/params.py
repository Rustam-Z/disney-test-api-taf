"""
Query string parameters.

Example:
    URL/?key=value -> here `key` is the query string parameter.

"""

from enum import Enum


class Param(Enum):
    IS_FOR_MOBILE = 'is_for_mobile'
    SECTION = 'section'
