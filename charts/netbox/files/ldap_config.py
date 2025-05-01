"""
This file serves as a LDAP configuration for Netbox
https://netboxlabs.com/docs/netbox/en/stable/installation/6-ldap/#configuration
https://django-auth-ldap.readthedocs.io/en/latest/reference.html
"""

from functools import reduce
from importlib import import_module
from typing import Any

import ldap
import yaml
from django_auth_ldap.config import LDAPGroupQuery, LDAPSearch


def _load_yaml() -> None:
    """Load YAML from file"""
    with open("/run/config/netbox/ldap.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    globals().update(config)


def _read_secret(secret_name: str, secret_key: str, default: str | None = None) -> str | None:
    """Read secret from file"""
    try:
        secret = open(
            f"/run/secrets/{secret_name}/{secret_key}",
            "r",
            encoding="utf-8",
        )
    except EnvironmentError:
        return default
    with secret:
        return secret.readline().strip()


def _import_group_type(group_type_name: str) -> Any | None:
    """Import and return the group type based on name"""
    mod = import_module("django_auth_ldap.config")
    try:
        return getattr(mod, group_type_name)()
    except AttributeError:
        return None


AUTH_LDAP_USER_SEARCH_FILTER = None
AUTH_LDAP_GROUP_SEARCH_FILTER = None
AUTH_LDAP_REQUIRE_GROUP = None
AUTH_LDAP_USER_FLAGS_BY_GROUP = {}

_load_yaml()

# The following may be needed if you are binding to Active Directory.
AUTH_LDAP_CONNECTION_OPTIONS = {ldap.OPT_REFERRALS: 0}

# Set the DN and password for the NetBox service account if needed.
AUTH_LDAP_BIND_PASSWORD = _read_secret("netbox", "ldap_bind_password")

# This search ought to return all groups to which the user belongs.
# django_auth_ldap uses this to determine group
# heirarchy.
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    AUTH_LDAP_USER_SEARCH_BASEDN,
    ldap.SCOPE_SUBTREE,
    AUTH_LDAP_USER_SEARCH_FILTER or f"({AUTH_LDAP_USER_SEARCH_ATTR}=%(user)s)",
)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    AUTH_LDAP_GROUP_SEARCH_BASEDN,
    ldap.SCOPE_SUBTREE,
    AUTH_LDAP_GROUP_SEARCH_FILTER or f"(objectClass={AUTH_LDAP_GROUP_SEARCH_CLASS})",
)
AUTH_LDAP_GROUP_TYPE = _import_group_type(AUTH_LDAP_GROUP_TYPE)

# Define a group required to login.
if AUTH_LDAP_REQUIRE_GROUP_LIST:
    AUTH_LDAP_REQUIRE_GROUP = reduce(
        lambda query, group: query | LDAPGroupQuery(group),
        AUTH_LDAP_REQUIRE_GROUP_LIST,
        LDAPGroupQuery(""),
    )

# Define special user types using groups. Exercise great caution when assigning superuser status.
if AUTH_LDAP_REQUIRE_GROUP is not None:
    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active": AUTH_LDAP_REQUIRE_GROUP,
        "is_staff": reduce(
            lambda query, group: query | LDAPGroupQuery(group),
            AUTH_LDAP_IS_ADMIN_LIST,
            LDAPGroupQuery(""),
        ),
        "is_superuser": reduce(
            lambda query, group: query | LDAPGroupQuery(group),
            AUTH_LDAP_IS_SUPERUSER_LIST,
            LDAPGroupQuery(""),
        ),
    }
