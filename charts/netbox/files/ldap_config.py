###################################################################
#  This file serves as a LDAP configuration for Netbox            #
#  https://netboxlabs.com/docs/netbox/en/stable/configuration/    #
###################################################################

from functools import reduce
from importlib import import_module
from django_auth_ldap.config import LDAPSearch, LDAPGroupQuery

import yaml
import ldap

def _load_yaml():
    """Load YAML from file"""
    with open("/run/config/netbox/ldap.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    globals().update(config)

def _read_secret(secret_name: str, secret_key: str, default: str | None = None) -> str | None:
    """Read secret from file"""
    try:
        f = open(
          "/run/secrets/{name}/{key}".format(name=secret_name, key=secret_key),
          'r',
          encoding='utf-8'
        )
    except EnvironmentError:
        return default
    else:
        with f:
            return f.readline().strip()

# Import and return the group type based on string name
def _import_group_type(group_type_name):
    mod = import_module("django_auth_ldap.config")
    try:
        return getattr(mod, group_type_name)()
    except AttributeError:
        return None

_load_yaml()

# The following may be needed if you are binding to Active Directory.
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

# Set the DN and password for the NetBox service account if needed.
AUTH_LDAP_BIND_PASSWORD = _read_secret("netbox", "ldap_bind_password")

# This search ought to return all groups to which the user belongs. django_auth_ldap uses this to determine group
# heirarchy.
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    AUTH_LDAP_USER_SEARCH_BASEDN,
    ldap.SCOPE_SUBTREE,
    "(" + AUTH_LDAP_USER_SEARCH_ATTR + "=%(user)s)",
)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    AUTH_LDAP_GROUP_SEARCH_BASEDN,
    ldap.SCOPE_SUBTREE,
    "(objectClass=" + AUTH_LDAP_GROUP_SEARCH_CLASS + ")",
)
AUTH_LDAP_GROUP_TYPE = _import_group_type(AUTH_LDAP_GROUP_TYPE)

# Define a group required to login.
AUTH_LDAP_REQUIRE_GROUP = reduce(lambda x, y: x | LDAPGroupQuery(y), AUTH_LDAP_REQUIRE_GROUP_LIST, False)

# Define special user types using groups. Exercise great caution when assigning superuser status.
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": reduce(lambda x, y: x | LDAPGroupQuery(y), AUTH_LDAP_REQUIRE_GROUP_LIST, False),
    "is_staff": reduce(lambda x, y: x | LDAPGroupQuery(y), AUTH_LDAP_IS_ADMIN_LIST, False),
    "is_superuser": reduce(lambda x, y: x | LDAPGroupQuery(y), AUTH_LDAP_IS_SUPERUSER_LIST, False),
}
