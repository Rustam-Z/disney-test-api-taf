"""
Authz = authorization.
Authn = authentication.
"""

from enum import Enum


class Authz(Enum):
    NONE = None  # Unauthenticated user.
    SUPERUSER = 'superuser'
    FACILITY_ADMIN = 'facility_admin'
    FACILITY_DRIVER = 'facility_driver'
    FACILITY_USER = 'facility_user'
