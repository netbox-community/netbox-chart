# Authentication Options

## Using SSO

You can configure different SSO backends with `remoteAuth`.
The implementation is based on [Python Social Auth](https://python-social-auth.readthedocs.io/en/latest/backends/index.html#supported-backends).

Depending on the chosen backend you may need to configure different parameters.
You can leverage the `extraConfig` value in conjunction with `remoteAuth`.

> [!tip]
> Read more about `extraConfig` usage within [Extra Configuration](./extra.md) guide.

By default the users do not have any permission after logging in.
Using custom auth pipelines you can assign groups based on the roles supplied by the oauth provider.

### Example config for Keycloak backend

```yaml
remoteAuth:
  enabled: true
  backends:
    - social_core.backends.keycloak.KeycloakOAuth2
  autoCreateUser: true

extraConfig:
  - secret:
      secretName: keycloak-client
  - values:
      SOCIAL_AUTH_PIPELINE:
        [
          "social_core.pipeline.social_auth.social_details",
          "social_core.pipeline.social_auth.social_uid",
          "social_core.pipeline.social_auth.social_user",
          "social_core.pipeline.user.get_username",
          "social_core.pipeline.social_auth.associate_by_email",
          "social_core.pipeline.user.create_user",
          "social_core.pipeline.social_auth.associate_user",
          "netbox.authentication.user_default_groups_handler",
          "social_core.pipeline.social_auth.load_extra_data",
          "social_core.pipeline.user.user_details",
          "netbox.sso_pipeline_roles.set_role",
        ]

extraVolumes:
  - name: sso-pipeline-roles
    configMap:
      name: sso-pipeline-roles
extraVolumeMounts:
  - name: sso-pipeline-roles
    mountPath: /opt/netbox/netbox/netbox/sso_pipeline_roles.py
    subPath: sso_pipeline_roles.py
    readOnly: true
```

Additional resources are necessary:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: keycloak-client
  namespace: netbox
type: Opaque
data:
  oidc-keycloak.yaml: |
    SOCIAL_AUTH_KEYCLOAK_KEY:               <OAUTH_CLIENT_ID>
    SOCIAL_AUTH_KEYCLOAK_SECRET:            <OAUTH_CLIENT_SECRET>
    SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY:        MIIB...AB
    SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL: "https://keycloak.example.com/auth/realms/master/protocol/openid-connect/auth"
    SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL:  "https://keycloak.example.com/auth/realms/master/protocol/openid-connect/token"
    SOCIAL_AUTH_JSONFIELD_ENABLED:          true
    SOCIAL_AUTH_STAFF_ROLE:                 staff
    SOCIAL_AUTH_SUPERUSER_ROLE:             superuser

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: sso-pipeline-roles
  namespace: netbox
data:
  sso_pipeline_roles.py: |
    from django.conf import settings
    from netbox.authentication import Group

    def set_role(response, user, backend, *args, **kwargs):
      client_id = getattr(settings, 'SOCIAL_AUTH_KEYCLOAK_KEY', None)
      staff_role = getattr(settings, 'SOCIAL_AUTH_STAFF_ROLE', 'staff')
      superuser_role = getattr(settings, 'SOCIAL_AUTH_SUPERUSER_ROLE', 'superuser')

      roles = []
      try:
        roles = response['resource_access'][client_id]['roles']
      except KeyError:
        pass
      user.is_staff = (staff_role in roles)
      user.is_superuser = (superuser_role in roles)
      user.save()
      groups = Group.objects.all()
      for group in groups:
        try:
          if group.name in roles:
            group.users.add(user)
          else:
            group.users.remove(user)
        except Group.DoesNotExist:
          continue
```

> [!note]
> A hardcoded custom audience mapper is required on Keycloak.
>
> For the audience name to be in the token, enter the Client ID
> in the _Included **Custom** Audience_ field instead of the _Included **Client** Audience_ field.
>
> Refer to the Keycloak usage materials:
>
> - [Python Social Auth Documentation](https://python-social-auth.readthedocs.io/en/latest/backends/keycloak.html)
> - [Python Social Auth Source Code](https://github.com/python-social-auth/social-core/blob/d9554fa40e751c85ae60231fe2f5bd5a528c4452/social_core/backends/keycloak.py#L7-L96)
> - [Keycloak Documentation](https://www.keycloak.org/docs/latest/server_admin/#_audience_hardcoded)

### Example config for GitLab backend

```yaml
remoteAuth:
  enabled: true
  backends:
    - social_core.backends.gitlab.GitLabOAuth2
  autoCreateUser: true

extraConfig:
  - secret:
      secretName: gitlab-client
  - values:
      SOCIAL_AUTH_PIPELINE:
        [
            "social_core.pipeline.social_auth.social_details",
            "social_core.pipeline.social_auth.social_uid",
            "social_core.pipeline.social_auth.social_user",
            "social_core.pipeline.user.get_username",
            "social_core.pipeline.social_auth.associate_by_email",
            "social_core.pipeline.user.create_user",
            "social_core.pipeline.social_auth.associate_user",
            "netbox.authentication.user_default_groups_handler",
            "social_core.pipeline.social_auth.load_extra_data",
            "social_core.pipeline.user.user_details",
            "netbox.sso_pipeline_roles.set_role",
        ]
extraVolumes:
  - name: sso-pipeline-roles
    configMap:
      name: sso-pipeline-roles
extraVolumeMounts:
  - name: sso-pipeline-roles
    mountPath: /opt/netbox/netbox/netbox/sso_pipeline_roles.py
    subPath: sso_pipeline_roles.py
    readOnly: true
```

Additional resources are necessary (please note that the client ID is necessary in the custom pipeline script):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gitlab-client
  namespace: netbox
type: Opaque
stringData:
  oidc-gitlab.yaml: |
    SOCIAL_AUTH_GITLAB_API_URL: https://git.example.com
    SOCIAL_AUTH_GITLAB_AUTHORIZATION_URL: https://git.example.com/oauth/authorize
    SOCIAL_AUTH_GITLAB_ACCESS_TOKEN_URL: https://git.example.com/oauth/token
    SOCIAL_AUTH_GITLAB_KEY: <OAUTH_CLIENT_ID>
    SOCIAL_AUTH_GITLAB_SECRET: <OAUTH_CLIENT_SECRET>
    SOCIAL_AUTH_GITLAB_SCOPE: ['read_user', 'openid']
    SOCIAL_AUTH_STAFF_ROLE:                 staff
    SOCIAL_AUTH_SUPERUSER_ROLE:             superuser

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: sso-pipeline-roles
  namespace: netbox
data:
  sso_pipeline_roles.py: |
    from django.conf import settings
    from netbox.authentication import Group

    import jwt
    from jwt import PyJWKClient
    def set_role(response, user, backend, *args, **kwargs):
      client_id = getattr(settings, 'SOCIAL_AUTH_GITLAB_KEY', None)
      staff_role = getattr(settings, 'SOCIAL_AUTH_STAFF_ROLE', 'staff')
      superuser_role = getattr(settings, 'SOCIAL_AUTH_SUPERUSER_ROLE', 'superuser')

      jwks_client = PyJWKClient("https://git.example.com/oauth/discovery/keys")
      signing_key = jwks_client.get_signing_key_from_jwt(response['id_token'])
      decoded = jwt.decode(
          response['id_token'],
          signing_key.key,
          algorithms=["RS256"],
          audience=client_id,
      )
      roles = []
      try:
        roles = decoded.get('groups_direct')
      except KeyError:
        pass
      user.is_staff = (staff_role in roles)
      user.is_superuser = (superuser_role in roles)
      user.save()
      groups = Group.objects.all()
      for group in groups:
        try:
          if group.name in roles:
            group.users.add(user)
          else:
            group.users.remove(user)
        except Group.DoesNotExist:
          continue
```

## Using LDAP Authentication

In order to enable LDAP authentication, please carry out the following steps:

1. Configure the `remoteAuth` settings to enable the LDAP backend (see below)
2. Make sure you set _all_ of the `remoteAuth.ldap` settings shown in the `values.yaml` file

For example:

```yaml
remoteAuth:
  enabled: true
  backends:
    - netbox.authentication.LDAPBackend
  ldap:
    serverUri: ldap://domain.com
    startTls: true
    ignoreCertErrors: true
    bindDn: ""
    bindPassword: ""
    # and ALL the other remoteAuth.ldap.* settings from values.yaml
```

> [!NOTE]
> In order to use anonymous LDAP binding, set `bindDn` and `bindPassword`
> to an empty string as in the example above.

### LDAP Certificate Verification

If you need to specify your own CA certificate, follow the instructions below.

#### Option 1. In your `values.yaml` file define the directory already containing your CA certificate

```yaml
  ldap:
    serverUri: ldap://domain.com
    startTls: true
    ignoreCertErrors: false
    caCertDir: /etc/ssl/certs
```

#### Option 2. In your `values.yaml` file define your CA certificate content in `caCertData`

```yaml
  ldap:
    serverUri: ldap://domain.com
    startTls: true
    ignoreCertErrors: false
    caCertData: |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----
```
