"""
The list of environments where we can perform testing.
The list of environments should be synchronized with the configuration file (.config.yaml).
"""

from enum import Enum


class Environment(Enum):
    DEV = 'dev'
