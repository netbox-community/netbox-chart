{{- define "netbox.ldap_config" -}}
import ldap
from django_auth_ldap.config import LDAPSearch, {{ .Values.ldap.auth_group_type }}

# Server URI
AUTH_LDAP_SERVER_URI = {{ .Values.ldap.server_uri | quote}}

# The following may be needed if you are binding to Active Directory.
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

# Set the DN and password for the NetBox service account.
AUTH_LDAP_BIND_DN = {{ .Values.ldap.bind_dn | quote}}
AUTH_LDAP_BIND_PASSWORD = {{ .Values.ldap.bind_password | quote }}

# Include this setting if you want to ignore certificate errors. This might be needed to accept a self-signed cert.
# Note that this is a NetBox-specific setting which sets:
#     ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
LDAP_IGNORE_CERT_ERRORS = {{ .Values.ldap.ignore_certificate_errors | title }}


# This search matches users with the sAMAccountName equal to the provided username. This is required if the user's
# username is not in their DN (Active Directory).
AUTH_LDAP_USER_SEARCH = LDAPSearch({{ .Values.ldap.auth_user_search_base | quote }},
                                    ldap.SCOPE_{{ .Values.ldap.auth_user_search_scope }}, "(sAMAccountName=%(user)s)")

# If a user's DN is producible from their username, we don't need to search.
AUTH_LDAP_USER_DN_TEMPLATE = {{ eq .Values.ldap.auth_user_dn_template "None" | ternary "None" (.Values.ldap.auth_user_dn_template | quote) }}

# You can map user attributes to Django attributes as so.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

# This search ought to return all groups to which the user belongs. django_auth_ldap uses this to determine group
# hierarchy.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch({{ .Values.ldap.auth_group_search_base | quote }}, ldap.SCOPE_{{ .Values.ldap.auth_group_search_scope }},
                                    "(objectClass=group)")

AUTH_LDAP_GROUP_TYPE = {{ .Values.ldap.auth_group_type }}()

# Define a group required to login.
AUTH_LDAP_REQUIRE_GROUP = {{ .Values.ldap.auth_require_group | quote }}

# Mirror LDAP group assignments.
AUTH_LDAP_MIRROR_GROUPS = True

# Define special user types using groups. Exercise great caution when assigning superuser status.
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": {{ .Values.ldap.auth_user_flags_by_group.is_active | quote}},
    "is_staff": {{ .Values.ldap.auth_user_flags_by_group.is_staff | quote}},
    "is_superuser": {{ .Values.ldap.auth_user_flags_by_group.is_superuser | quote}}
}

# For more granular permissions, we can map LDAP groups to Django groups.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache groups for one hour to reduce LDAP traffic
AUTH_LDAP_CACHE_TIMEOUT = 3600
{{ end }}