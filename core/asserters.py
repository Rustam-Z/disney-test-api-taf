from core.enums.assertion_message import AssertionMessage


class APIResponse:
    def __init__(self, response):
        self._response = response

    def body(self):
        return self._response.json()

    def check_status(self, status_code: int):
        assert self._response.status_code == status_code, AssertionMessage.WRONG_STATUS_CODE.value

    def check_model_values(self, request_model: dict):
        response_model = self._response.json()
        common_keys = set(request_model.keys()) & set(response_model.keys())  # Response may include entity `id`
        return all(request_model[key] == response_model[key] for key in common_keys)
