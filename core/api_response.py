from core.enums.assertion_enums import AssertionEnums


class APIResponse:
    def __init__(self, response):
        self._response = response

    def body(self):
        return self._response.json()

    def check_status(self, status_code: int):
        assert self._response.status_code == status_code, AssertionEnums.WRONG_STATUS_CODE.value
