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

    # Pagination and search.
    SEARCH = 'search'
    PAGE = 'page'
    PAGE_SIZE = 'page_size'

    IS_DRIVER = 'is_driver'
    DATE_START_TIME_UTC = 'date_start_time_utc'
    CUSTOMER_BARCODE = 'customer_barcode'
    ORDER_ID = 'order_id'
    DRIVER_ID = 'driver_id'
    CONFIG_QR_CODE = 'config_qr_code'
    ACTION = 'action'
