"""
Generates .config yaml file using config-template.yaml for CI/CD.
"""

import yaml
import os


def generate_config_file() -> None:
    with open('config-template.yaml', 'r') as f:
        template = yaml.safe_load(f)

        dev_env = template['dev']
        dev_env_users = dev_env['users']

        dev_env_users['superuser'][0]['email'] = os.environ.get('DEV_SUPERUSER_EMAIL', '')
        dev_env_users['superuser'][0]['password'] = os.environ.get('PASSWORD', '')
        dev_env_users['facility_admin'][0]['email'] = os.environ.get('DEV_FACILITY_ADMIN_EMAIL', '')
        dev_env_users['facility_admin'][0]['password'] = os.environ.get('PASSWORD', '')
        dev_env_users['facility_driver'][0]['email'] = os.environ.get('DEV_FACILITY_DRIVER_EMAIL', '')
        dev_env_users['facility_driver'][0]['password'] = os.environ.get('PASSWORD', '')
        dev_env_users['facility_user'][0]['email'] = os.environ.get('DEV_FACILITY_USER_EMAIL', '')
        dev_env_users['facility_user'][0]['password'] = os.environ.get('PASSWORD', '')

    with open('.config.yaml', 'w') as f:
        yaml.dump(template, f)

    print(f'New config file written to {os.getcwd()}/.config.yaml')


if __name__ == '__main__':
    generate_config_file()
