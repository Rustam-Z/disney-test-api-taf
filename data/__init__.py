from data.custom_faker import CustomFaker
from data.request_models_faker import RequestModelsFaker
from data.users import get_config_user

fake = CustomFaker()
fake.model = RequestModelsFaker()
