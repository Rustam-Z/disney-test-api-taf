"""
Authorized user types.
The values in User enum fields should be synchronized with the configuration file (.config.yaml).

NOTE!
    Authz = authorization.
    Authn = authentication.
"""

from enum import Enum


class User(Enum):
    NONE = None  # Unauthenticated user.
    SUPERUSER = 'superuser'
    FACILITY_ADMIN = 'facility_admin'
    FACILITY_DRIVER = 'facility_driver'
    FACILITY_USER = 'facility_user'
