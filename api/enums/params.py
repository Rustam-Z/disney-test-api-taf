"""
Query string parameters.

Example:
    URL/?key=value -> here `key` is the query string parameter.

"""

from enum import Enum


class Param(Enum):
    IS_FOR_MOBILE = 'is_for_mobile'
    SECTION = 'section'
    FACILITY = 'facility'
    CUSTOMER = 'customer'
    SEARCH = 'search'
    PAGE = 'page'
    PAGE_SIZE = 'page_size'
    IS_DRIVER = 'is_driver'
    DATE_START_TIME_UTC = 'date_start_time_utc'
