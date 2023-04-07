from json import JSONDecodeError

from core.enums.assertion_message import AssertionMessage


class APIResponse:
    def __init__(self, response):
        self._response = response

    def body(self):
        return self._response.text

    def json_body(self):
        return self._response.json()

    def assert_body_is_json(self):
        try:
            self.json_body()
        except JSONDecodeError:
            raise ValueError(f'Response body is not a JSON object.')
        except Exception as e:
            raise ValueError(f"Error: {e}")

    def assert_status(self, status_code: int):
        assert self._response.status_code == status_code, AssertionMessage.WRONG_STATUS_CODE.value

    def assert_body(self, request_body: dict | str):
        try:
            response_model = self.json_body()
            common_keys = set(request_body.keys()) & set(response_model.keys())  # Only asserting common keys.
            assert all(request_body.get(key) == response_model.get(key) for key in common_keys)
        except JSONDecodeError:
            response_text = self.body()
            assert response_text == request_body
        except Exception as e:
            raise ValueError(f"Error: {e}")
