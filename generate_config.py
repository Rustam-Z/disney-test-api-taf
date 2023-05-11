"""
Generates .config yaml file using config-template.yaml for CI/CD.
"""

import yaml
import os


print(os.environ.get('vars.DEV_FACILITY_ADMIN_EMAIL'))
print(os.environ.get('vars.DEV_FACILITY_DRIVER_EMAIL'))
print(os.environ.get('vars.DEV_FACILITY_USER_EMAIL'))
print(os.environ.get('secrets.PASSWORD'), os.environ.get('env.PASSWORD'))
print(os.environ.get('secrets.DEV_ENV'))



def main() -> None:
    with open('config-template.yaml', 'r') as f:
        template = yaml.safe_load(f)

    with open('.config.yaml', 'w') as f:
        yaml.dump(template, f)

    print(f'New config file written to {os.getcwd()}/.config.yaml')


if __name__ == '__main__':
    main()
