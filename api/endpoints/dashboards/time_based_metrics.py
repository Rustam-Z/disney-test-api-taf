from api.enums.params import Param
from api.enums.sections import Section
from core.http_client import HTTPClient
from api.response_models.response_models import ErrorResponse


class TimeBasedMetricsDashboardAPI:
    DASHBOARD = '/dashboard/metro-timing-logs/'

    def __init__(self, client: HTTPClient):
        self.client = client
        self.params = {
            Param.SECTION.value: Section.DASHBOARD.value
        }

    def get_aging_metros(self, **kwargs) -> tuple:
        ...

    def get_aging_metros_chart(self, **kwargs) -> tuple:
        ...

    def get_aging_metros_table(self, **kwargs) -> tuple:
        ...

    def get_staged_metros(self, **kwargs) -> tuple:
        ...
