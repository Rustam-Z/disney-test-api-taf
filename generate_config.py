"""
Generates .config yaml file using config-template.yaml for CI/CD.
"""

import yaml
import os


print(os.environ.get('DEV_FACILITY_ADMIN_EMAIL'))
print(os.environ.get('DEV_FACILITY_DRIVER_EMAIL'))
print(os.environ.get('DEV_FACILITY_USER_EMAIL'))
print(os.environ.get('PASSWORD'))


def main() -> None:
    with open('config-template.yaml', 'r') as f:
        template = yaml.safe_load(f)

    with open('.config.yaml', 'w') as f:
        yaml.dump(template, f)

    print(f'New config file written to {os.getcwd()}/.config.yaml')


if __name__ == '__main__':
    main()
