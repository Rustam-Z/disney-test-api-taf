"""
Generates .config yaml file using config-template.yaml. Creates test data and populates config file.
The structure of config file is described in config-template.yaml.
"""

import os
from collections import defaultdict

import yaml

from decouple import config

from api.endpoints.customer.customer_api import CustomerAPI
from api.endpoints.facility.facility_api import FacilityAPI
from api.endpoints.user.menu_api import MenuAPI
from api.endpoints.user.role_api import RoleAPI
from api.endpoints.user.users_api import UsersAPI
from core.auth import get_access_token
from core.enums.environments import Environment
from core.enums.users import User
from core.http_client import HTTPClient

CONFIG_FILE_TEMPLATE_PATH = 'config-template.yaml'
CONFIG_FILE_PATH = '.config.yaml'


def create_config_file():
    """
    Creates empty config file with default values using config template file.
    """
    with open(CONFIG_FILE_TEMPLATE_PATH, 'r') as f:
        data = yaml.safe_load(f)

    with open(CONFIG_FILE_PATH, 'w') as f:
        yaml.dump(data, f)


def is_data_exists(data: dict) -> bool:
    """
    Checks if email and passwords provided in config file contain valid values.
    If any values are invalid function returns.
    """
    env = data.get('env')
    env_users = data.get(env).get('users')

    for key, value_list in env_users.items():
        for item in value_list:
            email = item.get('email')
            password = item.get('password')
            if not email or not password:
                return False
    return True


def superadmin_create_users(email: str, password: str, api_url: str) -> dict:
    """
    Create HTTP client, authorize superadmin, create data.
    """
    import data

    # Create HTTP client and authorize superuser.
    client = HTTPClient(api_url)
    access_token = get_access_token(client, email, password)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    client.update_headers(headers)

    # Create customer.
    _payload = data.fake.model.customer()
    customer_response, customer_model = CustomerAPI(client).create_customer(data=_payload)

    # Create facility.
    _payload = data.fake.model.facility(customers=[customer_model.data.id])
    facility_response, facility_model = FacilityAPI(client).create_facility(data=_payload)
    facility_id = facility_model.data.id

    # Get menu list, based on this we will give permissions to users.
    menu_list_response, menu_list_model = MenuAPI(client).get_menu_list()

    role_sections = {
        User.FACILITY_ADMIN.value: {
            'sections': [
                section for section in menu_list_model.data.results if section.route not in [
                    'facility', 'customers', 'inventory-item-type', 'inventory-category'
                ]
            ],
        },
        User.FACILITY_DRIVER.value: {
            'sections': [
                section for section in menu_list_model.data.results if section.route in [
                    'cart_build', 'driver-process', 'metro-decommission',
                    'staging', 'metro-commission', 'metro-item-configuration'
                ]
            ],
            'is_driver': True
        },
        User.FACILITY_USER.value: {
            'sections': []
        }
    }

    credentials = defaultdict(list)
    for key, value in role_sections.items():
        # Create role.
        payload = data.fake.model.role(facility_id=facility_id, **value)
        role_response, role_model = RoleAPI(client).create_role(data=payload)
        role_id = role_model.data.id

        # Create user.
        payload = data.fake.model.user(role_id=role_id, facility_id=facility_id)
        users_response, users_model = UsersAPI(client).create_user(data=payload)
        email = payload.get('email')
        password = payload.get('password')

        credentials[key].append({'email': email, 'password': password})

    return credentials


def populate_data() -> None:
    """
    Populating data in the config file. Populating means, creating test data using APIs.
    """
    with open(CONFIG_FILE_PATH, 'r') as f:
        data = yaml.safe_load(f)  # dict

        env = data.get('env')
        env_users = data.get(env).get('users')
        env_api_url = data.get(env).get('hosts').get('api') + data.get('prefix')

        superadmin_email, superadmin_password = config('DEV_SUPERUSER_EMAIL'), config('DEV_SUPERUSER_PASSWORD')

        new_users = superadmin_create_users(superadmin_email, superadmin_password, env_api_url)

        if env == Environment.DEV.value:
            new_users.update({
                User.SUPERUSER.value: [{'email':  superadmin_email, 'password': superadmin_password}]
            })
        else:
            raise Exception("Only DEV environment is supported for now.")

        env_users.update(new_users)

    with open(CONFIG_FILE_PATH, 'w') as f:
        yaml.dump(data, f)


def main():
    if not os.path.exists(CONFIG_FILE_PATH):  # Checking if config file exists.
        create_config_file()

    with open(CONFIG_FILE_PATH, 'r') as file:
        data = yaml.safe_load(file)

        if not is_data_exists(data):  # Checking is data exists.
            populate_data()


if __name__ == '__main__':
    main()
