"""
Generates .config yaml file using config-template.yaml for CI/CD.
"""

import yaml
import os


def main() -> None:
    with open('config-template.yaml', 'r') as f:
        template = yaml.safe_load(f)

    with open('.config.yaml', 'w') as f:
        yaml.dump(template, f)

    print(f'New config file written to {os.getcwd()}/.config.yaml')


if __name__ == '__main__':
    main()
