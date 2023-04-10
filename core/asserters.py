from json import JSONDecodeError

from core.enums.assertion_message import AssertionMessage


class APIResponse:
    def __init__(self, response):
        self.response = response

    def body_str(self):
        return self.response.text

    def body_json(self):
        return self.response.json()

    def assert_body_is_json(self):
        try:
            self.body_json()
        except JSONDecodeError:
            raise ValueError(f'Response body is not a JSON object.')
        except Exception as e:
            raise ValueError(f"Error: {e}")

    def assert_status(self, status_code: int):
        assert self.response.status_code == status_code, \
            f'{AssertionMessage.WRONG_STATUS_CODE.value} Actual: {self.response.status_code}, expected: {status_code}.'

    def assert_models(self, request_body: dict | str):
        try:
            response_model = self.body_json().get('data')
            common_keys = set(request_body.keys()) & set(response_model.keys())  # Only asserting common keys.
            assert all(request_body.get(key) == response_model.get(key) for key in common_keys)
        except JSONDecodeError:
            return ValueError('Response object is not JSON.')
        except Exception as e:
            return ValueError(f"Error: {e}.")
