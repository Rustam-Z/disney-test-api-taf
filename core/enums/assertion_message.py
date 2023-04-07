from enum import Enum


class AssertionMessage(Enum):
    WRONG_STATUS_CODE = 'Status code is different than expected.'
    RESPONSE_HEADERS = 'Expected response headers discrepancy.'
    JSON_ELEMENT_VALUE = 'JSON element value is different than expected.'
    JSON_DOES_NOT_CONTAIN = "Element doesn't contain given values."
    JSON_ELEMENTS_COUNT = 'Expected count of elements is different than expected.'
    JSON_ELEMENT_NOT_EXIST = "Expected element is not found in JSON response."
    JSON_ELEMENT_VALUE_NOT_EXIST = "JSON element value doesn't exist"
