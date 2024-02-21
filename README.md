# NetBox

[NetBox](https://netbox.readthedocs.io/) is an IP address management (IPAM) and
data center infrastructure management (DCIM) tool.

## TL;DR

```shell
$ helm repo add bootc https://charts.boo.tc
$ helm install netbox \
  --set postgresql.auth.postgresPassword=[password1] \
  --set postgresql.auth.password=[password2] \
  --set redis.auth.password=[password3] \
  bootc/netbox
```
⚠️ **WARNING:** Please see [Production Usage](#production-usage) below before using this chart for real.

## Prerequisites

- Kubernetes 1.25.0+ (a [current](https://kubernetes.io/releases/) version)
- Helm 3.10.0+ (a version [compatible](https://helm.sh/docs/topics/version_skew/) with your cluster)
- This chart works with NetBox 3.5.0+ (3.6.4+ recommended)

## Installing the Chart

To install the chart with the release name `my-release` and default configuration:

```shell
$ helm repo add bootc https://charts.boo.tc
$ helm install my-release \
  --set postgresql.auth.postgresPassword=[password1] \
  --set postgresql.auth.password=[password2] \
  --set redis.auth.password=[password3] \
  bootc/netbox
```

The default configuration includes the required PostgreSQL and Redis database
services, but both should be managed externally in production deployments; see below.

### Production Usage

Always [use an existing Secret](#using-an-existing-secret) and supply all
passwords and secret keys yourself to avoid Helm re-generating any of them for
you.

I strongly recommend setting both `postgresql.enabled` and `redis.enabled` to
`false` and using a separate external PostgreSQL and Redis instance. This
de-couples those services from the chart's bundled versions which may have
complex upgrade requirements. I also recommend using a clustered PostgreSQL
server (e.g. using Zalando's
[Postgres Operator](https://github.com/zalando/postgres-operator)) and Redis
with Sentinel (e.g. using [Aaron Layfield](https://github.com/DandyDeveloper)'s
[redis-ha chart](https://github.com/DandyDeveloper/charts/tree/master/charts/redis-ha)).

Set `persistence.enabled` to `false` and use the S3 `storageBackend` for object
storage. This works well with Minio or Ceph RGW as well as Amazon S3. See [Using extraConfig for S3 storage configuration](#using-extraconfig-for-s3-storage-configuration) and [Persistent storage pitfalls](#persistent-storage-pitfalls), below.

Run multiple replicas of the NetBox web front-end to avoid interruptions during
upgrades or at other times when the pods need to be restarted. There's no need
to have multiple workers (`worker.replicaCount`) for better availability. Set
up `affinity.podAntiAffinity` to avoid multiple NetBox pods being colocated on
the same node, for example:

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app.kubernetes.io/instance: netbox
            app.kubernetes.io/name: netbox
            app.kubernetes.io/component: netbox
        topologyKey: kubernetes.io/hostname
```

## Uninstalling the Chart

To delete the chart:

```shell
$ helm delete my-release
```

## Upgrading

### Bundled PostgreSQL

When upgrading or changing settings and using the bundled Bitnami PostgreSQL
sub-chart, you **must** provide the `postgresql.auth.password` at minimum.
Ideally you should also supply the `postgresql.auth.postgresPassword` and,
if using replication, the `postgresql.auth.replicationPassword`. Please see the
[upstream documentation](https://github.com/bitnami/charts/tree/master/bitnami/postgresql#upgrading)
for further information.

### From 4.x to 5.x

* NetBox has been updated to 3.6.4, but older 3.5+ versions should still work (this is not tested or supported, however).
* **Potentially breaking changes:**
  * The `jobResultRetention` setting has been renamed `jobRetention` to match the change in NetBox 3.5.
  * The `remoteAuth.backend` setting has been renamed `remoteAuth.backends` and is now an array.
  * The `remoteAuth.autoCreateUser` setting now defaults to `false`.
  * NAPALM support has been moved into a plugin since NetBox 3.5, so all NAPALM configuration has been **removed from this chart**.
  * Please consult the [NetBox](https://docs.netbox.dev/en/stable/release-notes/) and [netbox-docker](https://github.com/netbox-community/netbox-docker) release notes in case there are any other changes that may affect your configuration.
* The Bitnami [PostgreSQL](https://github.com/bitnami/charts/tree/main/bitnami/postgresql) sub-chart was upgraded from 10.x to 13.x; please read the upstream upgrade notes if you are using the bundled PostgreSQL.
* The Bitnami [Redis](https://github.com/bitnami/charts/tree/main/bitnami/redis) sub-chart was upgraded from 15.x to 18.x; please read the upstream upgrade notes if you are using the bundled Redis.

### From 3.x to 4.x

* NetBox 3.0.0 or above is required
* The Bitnami [Redis](https://github.com/bitnami/charts/tree/master/bitnami/redis) sub-chart was upgraded from 12.x to 15.x; please read the upstream upgrade notes if you are using the bundled Redis
* The `cacheTimeout` and `releaseCheck.timeout` settings were removed

### From 2.x to 3.x

* NetBox 2.10.4 or above is required
* Kubernetes 1.14 or above is required
* Helm v3 or above is now required
* The `netbox` Deployment selectors are changed, so the Deployment **must** be deleted on upgrades
* The Bitnami [PostgreSQL](https://github.com/bitnami/charts/tree/master/bitnami/postgresql) sub-chart was upgraded from 8.x to 10.x; please read the upstream upgrade notes if you are using the bundled PostgreSQL
* The Bitnami [Redis](https://github.com/bitnami/charts/tree/master/bitnami/redis) sub-chart was upgraded from 10.x to 12.x; please read the upstream upgrade notes if you are using the bundled Redis
* The NGINX container is removed, on account of upstream's migration from Gunicorn to NGINX Unit
* The `webhooksRedis` configuration key in `values.yaml` has been renamed to `tasksRedis` to match the upstream name
* The `redis_password` key in the Secret has been renamed to `redis_tasks_password`

### From 1.x to 2.x

If you use an external Redis you will need to update your configuration values
due to the chart reflecting upstream changes in how it uses Redis. There are
now separate Redis configuration blocks for webhooks and for caching, though
they can both point at the same Redis instance as long as the database numbers
are different.

### From 0.x to 1.x

The chart dependencies on PostgreSQL and Redis have been upgraded, so you may
need to take action depending on how you have configured the chart. The
PostgreSQL chart was upgraded from 5.x.x to 7.x.x, and Redis from 8.x.x to
9.x.x.

## Configuration

The following table lists the configurable parameters for this chart and their default values.

| Parameter                                       | Description                                                         | Default                                      |
| ------------------------------------------------|---------------------------------------------------------------------|----------------------------------------------|
| `replicaCount`                                  | The desired number of NetBox pods                                   | `1`                                          |
| `image.repository`                              | NetBox container image repository                                   | `netboxcommunity/netbox`                     |
| `image.tag`                                     | NetBox container image tag                                          | `""`                                         |
| `image.pullPolicy`                              | NetBox container image pull policy                                  | `IfNotPresent`                               |
| `image.command`                                 | NetBox container image command/entrypoint                           | `[]`                                         |
| `image.args`                                    | NetBox container image args                                         | `[]`                                         |
| `superuser.name`                                | Initial super-user account to create                                | `admin`                                      |
| `superuser.email`                               | Email address for the initial super-user account                    | `admin@example.com`                          |
| `superuser.password`                            | Password for the initial super-user account                         | `admin`                                      |
| `superuser.apiToken`                            | API token created for the initial super-user account                | `0123456789abcdef0123456789abcdef01234567`   |
| `skipStartupScripts`                            | Skip [netbox-docker startup scripts]                                | `true`                                       |
| `allowedHosts`                                  | List of valid FQDNs for this NetBox instance                        | `["*"]`                                      |
| `admins`                                        | List of admins to email about critical errors                       | `[]`                                         |
| `allowTokenRetrieval`                           | Permit the retrieval of API tokens after their creation             | `false`                                      |
| `authPasswordValidators`                        | Configure validation of local user account passwords                | `[]`                                         |
| `allowedUrlSchemes`                             | URL schemes that are allowed within links in NetBox                 | *see `values.yaml`*                          |
| `banner.top`                                    | Banner text to display at the top of every page                     | `""`                                         |
| `banner.bottom`                                 | Banner text to display at the bottom of every page                  | `""`                                         |
| `banner.login`                                  | Banner text to display on the login page                            | `""`                                         |
| `basePath`                                      | Base URL path if accessing NetBox within a directory                | `""`                                         |
| `changelogRetention`                            | Maximum number of days to retain logged changes (0 = forever)       | `90`                                         |
| `customValidators`                              | Custom validators for NetBox field values                           | `{}`                                         |
| `defaultUserPreferences`                        | Default preferences for newly created user accounts                 | `{}`                                         |
| `cors.originAllowAll`                           | [CORS]: allow all origins                                           | `false`                                      |
| `cors.originWhitelist`                          | [CORS]: list of origins authorised to make cross-site HTTP requests | `[]`                                         |
| `cors.originRegexWhitelist`                     | [CORS]: list of regex strings matching authorised origins           | `[]`                                         |
| `csrf.cookieName`                               | Name of the CSRF authentication cookie                              | `csrftoken`                                  |
| `csrf.trustedOrigins`                           | A list of trusted origins for unsafe (e.g. POST) requests           | `[]`                                         |
| `debug`                                         | Enable NetBox debugging (NOT for production use)                    | `false`                                      |
| `defaultLanguage`                               | Set the default preferred language/locale                           | `en-us`                                      |
| `dbWaitDebug`                                   | Show details of errors that occur when applying migrations          | `false`                                      |
| `email.server`                                  | SMTP server to use to send emails                                   | `localhost`                                  |
| `email.port`                                    | TCP port to connect to the SMTP server on                           | `25`                                         |
| `email.username`                                | Optional username for SMTP authentication                           | `""`                                         |
| `email.password`                                | Password for SMTP authentication (see also `existingSecret`)        | `""`                                         |
| `email.useSSL`                                  | Use SSL when connecting to the server                               | `false`                                      |
| `email.useTLS`                                  | Use TLS when connecting to the server                               | `false`                                      |
| `email.sslCertFile`                             | SMTP SSL certificate file path (e.g. in a mounted volume)           | `""`                                         |
| `email.sslKeyFile`                              | SMTP SSL key file path (e.g. in a mounted volume)                   | `""`                                         |
| `email.timeout`                                 | Timeout for SMTP connections, in seconds                            | `10`                                         |
| `email.from`                                    | Sender address for emails sent by NetBox                            | `""`                                         |
| `enforceGlobalUnique`                           | Enforce unique IP space in the global table (not in a VRF)          | `false`                                      |
| `exemptViewPermissions`                         | A list of models to exempt from the enforcement of view permissions | `[]`                                         |
| `fieldChoices`                                  | Configure custom choices for certain built-in fields                | `{}`                                         |
| `graphQlEnabled`                                | Enable the GraphQL API                                              | `true`                                       |
| `httpProxies`                                   | HTTP proxies NetBox should use when sending outbound HTTP requests  | `null`                                       |
| `internalIPs`                                   | IP addresses recognized as internal to the system                   | `['127.0.0.1', '::1']`                       |
| `jobRetention`                                  | The number of days to retain job results (scripts and reports)      | `90`                                         |
| `logging`                                       | Custom Django logging configuration                                 | `{}`                                         |
| `loginPersistence`                              | Enables users to remain authenticated to NetBox indefinitely        | `false`                                      |
| `loginRequired`                                 | Permit only logged-in users to access NetBox                        | `false` (unauthenticated read-only access)   |
| `loginTimeout`                                  | How often to re-authenticate users                                  | `1209600` (14 days)                          |
| `logoutRedirectUrl`                             | View name or URL to which users are redirected after logging out    | `home`                                       |
| `maintenanceMode`                               | Display a "maintenance mode" banner on every page                   | `false`                                      |
| `mapsUrl`                                       | The URL to use when mapping physical addresses or GPS coordinates   | `https://maps.google.com/?q=`                |
| `maxPageSize`                                   | Maximum number of objects that can be returned by a single API call | `1000`                                       |
| `storageBackend`                                | Django-storages backend class name                                  | `null`                                       |
| `storageConfig`                                 | Django-storages backend configuration                               | `{}`                                         |
| `metricsEnabled`                                | Expose Prometheus metrics at the `/metrics` HTTP endpoint           | `false`                                      |
| `paginateCount`                                 | The default number of objects to display per page in the web UI     | `50`                                         |
| `plugins`                                       | Additional plugins to load into NetBox                              | `[]`                                         |
| `pluginsConfig`                                 | Configuration for the additional plugins                            | `{}`                                         |
| `powerFeedDefaultAmperage`                      | Default amperage value for new power feeds                          | `15`                                         |
| `powerFeedMaxUtilisation`                       | Default maximum utilisation percentage for new power feeds          | `80`                                         |
| `powerFeedDefaultVoltage`                       | Default voltage value for new power feeds                           | `120`                                        |
| `preferIPv4`                                    | Prefer devices' IPv4 address when determining their primary address | `false`                                      |
| `rackElevationDefaultUnitHeight`                | Rack elevation default height in pixels                             | `22`                                         |
| `rackElevationDefaultUnitWidth`                 | Rack elevation default width in pixels                              | `220`                                        |
| `remoteAuth.enabled`                            | Enable remote authentication support                                | `false`                                      |
| `remoteAuth.backends`                           | Remote authentication backend classes                               | `[netbox.authentication.RemoteUserBackend]`  |
| `remoteAuth.header`                             | The name of the HTTP header which conveys the username              | `HTTP_REMOTE_USER`                           |
| `remoteAuth.userFirstName`                      | HTTP header which contains the user's first name                    | `HTTP_REMOTE_USER_FIRST_NAME`                |
| `remoteAuth.userLastName`                       | HTTP header which contains the user's last name                     | `HTTP_REMOTE_USER_LAST_NAME`                 |
| `remoteAuth.userEmail`                          | HTTP header which contains the user's email address                 | `HTTP_REMOTE_USER_EMAIL`                     |
| `remoteAuth.autoCreateUser`                     | Enables the automatic creation of new users                         | `false`                                      |
| `remoteAuth.autoCreateGroups`                   | Enables the automatic creation of new groups                        | `false`                                      |
| `remoteAuth.defaultGroups`                      | A list of groups to assign to newly created users                   | `[]`                                         |
| `remoteAuth.defaultPermissions`                 | A list of permissions to assign newly created users                 | `{}`                                         |
| `remoteAuth.groupSyncEnabled`                   | Sync remote user groups from an HTTP header set by a reverse proxy  | `false`                                      |
| `remoteAuth.groupHeader`                        | The name of the HTTP header which conveys the groups to which the user belongs | `HTTP_REMOTE_USER_GROUP`          |
| `remoteAuth.superuserGroups`                    | The list of groups that promote an remote User to Superuser on login| `[]`                                         |
| `remoteAuth.superusers`                         | The list of users that get promoted to Superuser on login           | `[]`                                         |
| `remoteAuth.staffGroups`                        | The list of groups that promote an remote User to Staff on login    | `[]`                                         |
| `remoteAuth.staffUsers`                         | The list of users that get promoted to Staff on login               | `[]`                                         |
| `remoteAuth.groupSeparator`                     | The Seperator upon which `remoteAuth.groupHeader` gets split into individual groups | `\|`                        |
| `remoteAuth.ldap.serverUri`                     | see [django-auth-ldap](https://django-auth-ldap.readthedocs.io)     | `""`                                         |
| `remoteAuth.ldap.startTls`                      | if StarTLS should be used                                           | *see values.yaml*                            |
| `remoteAuth.ldap.ignoreCertErrors`              | if Certificate errors should be ignored                             | *see values.yaml*                            |
| `remoteAuth.ldap.bindDn`                        | Distinguished Name to bind with                                     | `""`                                         |
| `remoteAuth.ldap.bindPassword`                  | Password for bind DN                                                | `""`                                         |
| `remoteAuth.ldap.userDnTemplate`                | see [AUTH_LDAP_USER_DN_TEMPLATE](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-dn-template) | *see values.yaml* |
| `remoteAuth.ldap.userSearchBaseDn`              | see base_dn of [django_auth_ldap.config.LDAPSearch](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#django_auth_ldap.config.LDAPSearch) | *see values.yaml* |
| `remoteAuth.ldap.userSearchAttr`                | User attribute name for user search                                 | `sAMAccountName`                             |
| `remoteAuth.ldap.groupSearchBaseDn`             | base DN for group search                                            | *see values.yaml*                            |
| `remoteAuth.ldap.groupSearchClass`              | [django-auth-ldap](https://django-auth-ldap.readthedocs.io) for group search | `group`                             |
| `remoteAuth.ldap.groupType`                     | see [AUTH_LDAP_GROUP_TYPE](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-group-type) | `GroupOfNamesType` |
| `remoteAuth.ldap.requireGroupDn`                | DN of a group that is required for login                            | `null`                                       |
| `remoteAuth.ldap.findGroupPerms`                | see [AUTH_LDAP_FIND_GROUP_PERMS](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-find-group-perms) | true |
| `remoteAuth.ldap.mirrorGroups`                  | see [AUTH_LDAP_MIRROR_GROUPS](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-mirror-groups) | `null` |
| `remoteAuth.ldap.cacheTimeout`                  | see [AUTH_LDAP_MIRROR_GROUPS_EXCEPT](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-mirror-groups-except) | `null` |
| `remoteAuth.ldap.isAdminDn`                     | required DN to be able to login in Admin-Backend, "is_staff"-Attribute of [AUTH_LDAP_USER_FLAGS_BY_GROUP](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-flags-by-group) | *see values.yaml* |
| `remoteAuth.ldap.isSuperUserDn`                 | required DN to receive SuperUser privileges, "is_superuser"-Attribute of [AUTH_LDAP_USER_FLAGS_BY_GROUP](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-flags-by-group) | *see values.yaml* |
| `remoteAuth.ldap.attrFirstName`                 | first name attribute of users, "first_name"-Attribute of [AUTH_LDAP_USER_ATTR_MAP](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-attr-map) | `givenName` |
| `remoteAuth.ldap.attrLastName`                  | last name attribute of users, "last_name"-Attribute of [AUTH_LDAP_USER_ATTR_MAP](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-attr-map) | `sn` |
| `remoteAuth.ldap.attrMail`                      | mail attribute of users, "email_name"-Attribute of [AUTH_LDAP_USER_ATTR_MAP](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-attr-map) | `mail` |
| `releaseCheck.url`                              | Release check URL (GitHub API URL; see `values.yaml`)               | `null` (disabled by default)                 |
| `rqDefaultTimeout`                              | Maximum execution time for background tasks, in seconds             | `300` (5 minutes)                            |
| `sessionCookieName`                             | The name to use for the session cookie                              | `"sessionid"`                                |
| `enableLocalization`                            | Localization                                                        | `false`                                      |
| `timeZone`                                      | The time zone NetBox will use when dealing with dates and times     | `UTC`                                        |
| `dateFormat`                                    | Django date format for long-form date strings                       | `"N j, Y"`                                   |
| `shortDateFormat`                               | Django date format for short-form date strings                      | `"Y-m-d"`                                    |
| `timeFormat`                                    | Django date format for long-form time strings                       | `"g:i a"`                                    |
| `serviceMonitor.enabled`                        | Whether to enable a [ServiceMonitor](https://prometheus-operator.dev/docs/operator/design/#servicemonitor) for Netbox | `false`                                      |
| `serviceMonitor.additionalLabels`               | Additonal labels to apply to the ServiceMonitor                     | `{}`                                         |
| `serviceMonitor.interval`                       | Interval to scrape metrics.                                         | `1m`                                         |
| `serviceMonitor.scrapeTimeout`                  | Timeout duration for scraping metrics                               | `10s`                                        |
| `shortTimeFormat`                               | Django date format for short-form time strings                      | `"H:i:s"`                                    |
| `dateTimeFormat`                                | Django date format for long-form date and time strings              | `"N j, Y g:i a"`                             |
| `shortDateTimeFormat`                           | Django date format for short-form date and time strongs             | `"Y-m-d H:i"`                                |
| `extraConfig`                                   | Additional NetBox configuration (see `values.yaml`)                 | `[]`                                         |
| `secretKey`                                     | Django secret key used for sessions and password reset tokens       | `""` (generated)                             |
| `existingSecret`                                | Use an existing Kubernetes `Secret` for secret values (see below)   | `""` (use individual chart values)           |
| `overrideUnitConfig`                            | Override the NGINX Unit application server configuration            | `{}` (*see values.yaml*)                     |
| `postgresql.enabled`                            | Deploy PostgreSQL using bundled Bitnami PostgreSQL chart            | `true`                                       |
| `postgresql.auth.username`                      | Username to create for NetBox in bundled PostgreSQL instance        | `netbox`                                     |
| `postgresql.auth.database`                      | Database to create for NetBox in bundled PostgreSQL instance        | `netbox`                                     |
| `postgresql.*`                                  | Values under this key are passed to the bundled PostgreSQL chart    | n/a                                          |
| `externalDatabase.host`                         | PostgreSQL host to use when `postgresql.enabled` is `false`         | `localhost`                                  |
| `externalDatabase.port`                         | Port number for external PostgreSQL                                 | `5432`                                       |
| `externalDatabase.database`                     | Database name for external PostgreSQL                               | `netbox`                                     |
| `externalDatabase.username`                     | Username for external PostgreSQL                                    | `netbox`                                     |
| `externalDatabase.password`                     | Password for external PostgreSQL (see also `existingSecret`)        | `""`                                         |
| `externalDatabase.existingSecretName`           | Fetch password for external PostgreSQL from a different `Secret`    | `""`                                         |
| `externalDatabase.existingSecretKey`            | Key to fetch the password in the above `Secret`                     | `postgresql-password`                        |
| `externalDatabase.sslMode`                      | PostgreSQL client SSL Mode setting                                  | `prefer`                                     |
| `externalDatabase.connMaxAge`                   | The lifetime of a database connection, as an integer of seconds     | `300`                                        |
| `externalDatabase.disableServerSideCursors`     | Disable the use of server-side cursors transaction pooling          | `false`                                      |
| `externalDatabase.targetSessionAttrs`           | Determines whether the session must have certain properties         | `read-write`                                 |
| `redis.enabled`                                 | Deploy Redis using bundled Bitnami Redis chart                      | `true`                                       |
| `redis.*`                                       | Values under this key are passed to the bundled Redis chart         | n/a                                          |
| `tasksRedis.database`                           | Redis database number used for NetBox task queue                    | `0`                                          |
| `tasksRedis.ssl`                                | Enable SSL when connecting to Redis                                 | `false`                                      |
| `tasksRedis.insecureSkipTlsVerify`              | Skip TLS certificate verification when connecting to Redis          | `false`                                      |
| `tasksRedis.caCertPath`                         | Path to CA certificates bundle for Redis (needs mounting manually)  | `""`                                         |
| `tasksRedis.host`                               | Redis host to use when `redis.enabled` is `false`                   | `"netbox-redis"`                             |
| `tasksRedis.port`                               | Port number for external Redis                                      | `6379`                                       |
| `tasksRedis.sentinels`                          | List of sentinels in `host:port` form (`host` and `port` not used)  | `[]`                                         |
| `tasksRedis.sentinelService`                    | Sentinel master service name                                        | `"netbox-redis"`                             |
| `tasksRedis.sentinelTimeout`                    | Sentinel connection timeout, in seconds                             | `300` (5 minutes)                            |
| `tasksRedis.username`                           | Username for external Redis                                         | `""`                                         |
| `tasksRedis.password`                           | Password for external Redis (see also `existingSecret`)             | `""`                                         |
| `tasksRedis.existingSecretName`                 | Fetch password for external Redis from a different `Secret`         | `""`                                         |
| `tasksRedis.existingSecretKey`                  | Key to fetch the password in the above `Secret`                     | `redis-password`                             |
| `cachingRedis.database`                         | Redis database number used for caching views                        | `1`                                          |
| `cachingRedis.ssl`                              | Enable SSL when connecting to Redis                                 | `false`                                      |
| `cachingRedis.insecureSkipTlsVerify`            | Skip TLS certificate verification when connecting to Redis          | `false`                                      |
| `cachingRedis.caCertPath`                       | Path to CA certificates bundle for Redis (needs mounting manually)  | `""`                                         |
| `cachingRedis.host`                             | Redis host to use when `redis.enabled` is `false`                   | `"netbox-redis"`                             |
| `cachingRedis.port`                             | Port number for external Redis                                      | `6379`                                       |
| `cachingRedis.sentinels`                        | List of sentinels in `host:port` form (`host` and `port` not used)  | `[]`                                         |
| `cachingRedis.sentinelService`                  | Sentinel master service name                                        | `"netbox-redis"`                             |
| `cachingRedis.sentinelTimeout`                  | Sentinel connection timeout, in seconds                             | `300` (5 minutes)                            |
| `cachingRedis.username`                         | Username for external Redis                                         | `""`                                         |
| `cachingRedis.password`                         | Password for external Redis (see also `existingSecret`)             | `""`                                         |
| `cachingRedis.existingSecretName`               | Fetch password for external Redis from a different `Secret`         | `""`                                         |
| `cachingRedis.existingSecretKey`                | Key to fetch the password in the above `Secret`                     | `redis-password`                             |
| `imagePullSecrets`                              | List of `Secret` names containing private registry credentials      | `[]`                                         |
| `nameOverride`                                  | Override the application name (`netbox`) used throughout the chart  | `""`                                         |
| `fullnameOverride`                              | Override the full name of resources created as part of the release  | `""`                                         |
| `serviceAccount.create`                         | Create a ServiceAccount for NetBox                                  | `true`                                       |
| `serviceAccount.annotations`                    | Annotations to add to the service account                           | `{}`                                         |
| `serviceAccount.name`                           | The name of the service account to use                              | `""` (use the fullname)                      |
| `serviceAccount.imagePullSecrets`               | Add an imagePullSecrets attribute to the serviceAccount             | `""`                                         |
| `serviceAccount.automountServiceAccountToken`   | Whether to automatically mount the token in the containers using this serviceAccount or not | `false`              |
| `persistence.enabled`                           | Enable storage persistence for uploaded media (images)              | `true`                                       |
| `persistence.existingClaim`                     | Use an existing `PersistentVolumeClaim` instead of creating one     | `""`                                         |
| `persistence.subPath`                           | Mount a sub-path of the volume into the container, not the root     | `""`                                         |
| `persistence.storageClass`                      | Set the storage class of the PVC (use `-` to disable provisioning)  | `""`                                         |
| `persistence.selector`                          | Set the selector for PVs, if desired                                | `{}`                                         |
| `persistence.accessMode`                        | Access mode for the volume                                          | `ReadWriteOnce`                              |
| `persistence.size`                              | Size of persistent volume to request                                | `1Gi`                                        |
| `reportsPersistence.enabled`                    | Enable storage persistence for NetBox reports                       | `false`                                      |
| `reportsPersistence.existingClaim`              | Use an existing `PersistentVolumeClaim` instead of creating one     | `""`                                         |
| `reportsPersistence.subPath`                    | Mount a sub-path of the volume into the container, not the root     | `""`                                         |
| `reportsPersistence.storageClass`               | Set the storage class of the PVC (use `-` to disable provisioning)  | `""`                                         |
| `reportsPersistence.selector`                   | Set the selector for PVs, if desired                                | `{}`                                         |
| `reportsPersistence.accessMode`                 | Access mode for the volume                                          | `ReadWriteOnce`                              |
| `reportsPersistence.size`                       | Size of persistent volume to request                                | `1Gi`                                        |
| `podAnnotations`                                | Additional annotations for NetBox pods                              | `{}`                                         |
| `podLabels`                                     | Additional labels for NetBox pods                                   | `{}`                                         |
| `podSecurityContext`                            | Security context for NetBox pods                                    | *see `values.yaml`*                          |
| `securityContext`                               | Security context for NetBox containers                              | *see `values.yaml`*                          |
| `service.type`                                  | Type of `Service` resource to create                                | `ClusterIP`                                  |
| `service.port`                                  | Port number for the service                                         | `80`                                         |
| `service.nodePort`                              | The port used on the node when `service.type` is NodePort           | `""`                                         |
| `service.clusterIP`                             | The cluster IP address assigned to the service                      | `""`                                         |
| `service.clusterIPs`                            | A list of cluster IP addresses assigned to the service              | `[]`                                         |
| `service.externalIPs`                           | A list of external IP addresses aliased to this service             | `[]`                                         |
| `service.externalTrafficPolicy`                 | Policy for routing external traffic                                 | `""`                                         |
| `service.ipFamilyPolicy`                        | Represents the dual-stack-ness of the service                       | `""`                                         |
| `service.loadBalancerIP`                        | Request a specific IP address when `service.type` is LoadBalancer   | `""`                                         |
| `service.loadBalancerSourceRanges`              | A list of allowed IP ranges when `service.type` is LoadBalancer     | `[]`                                         |
| `ingress.enabled`                               | Create an `Ingress` resource for accessing NetBox                   | `false`                                      |
| `ingress.className`                             | Use a named IngressClass                                            | `""`                                         |
| `ingress.annotations`                           | Extra annotations to apply to the `Ingress` resource                | `{}`                                         |
| `ingress.hosts`                                 | List of hosts and paths to map to the service (see `values.yaml`)   | `[{host:"chart-example.local",paths:["/"]}]` |
| `ingress.tls`                                   | TLS settings for the `Ingress` resource                             | `[]`                                         |
| `resources`                                     | Configure resource requests or limits for NetBox                    | `{}`                                         |
| `automountServiceAccountToken`                  | Whether to automatically mount the serviceAccount token in the main container or not | `false`                     |
| `topologySpreadConstraints`                     | Configure Pod Topology Spread Constraints for NetBox                | `[]`                                         |
| `readinessProbe.enabled`                        | Enable Kubernetes readinessProbe, see [readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes) | *see `values.yaml`* |
| `readinessProbe.initialDelaySeconds`            | Number of seconds                                                   |  *see `values.yaml`*                         |
| `readinessProbe.timeoutSeconds`                 | Number of seconds                                                   |  *see `values.yaml`*                         |
| `readinessProbe.periodSeconds`                  | Number of seconds                                                   |  *see `values.yaml`*                         |
| `readinessProbe.successThreshold`               | Number of seconds                                                   |  *see `values.yaml`*                         |
| `init.image.repository`                         | Init container image repository                                     | `busybox`                                    |
| `init.image.tag`                                | Init container image tag                                            | `1.32.1`                                     |
| `init.image.pullPolicy`                         | Init container image pull policy                                    | `IfNotPresent`                               |
| `init.resources`                                | Configure resource requests or limits for init container            | `{}`                                         |
| `init.securityContext`                          | Security context for init container                                 | *see `values.yaml`*                          |
| `autoscaling.enabled`                           | Whether to enable the HorizontalPodAutoscaler                       | `false`                                      |
| `autoscaling.minReplicas`                       | Minimum number of replicas when autoscaling is enabled              | `1`                                          |
| `autoscaling.maxReplicas`                       | Maximum number of replicas when autoscaling is enabled              | `100`                                        |
| `autoscaling.targetCPUUtilizationPercentage`    | Target CPU utilisation percentage for autoscaling                   | `80`                                         |
| `autoscaling.targetMemoryUtilizationPercentage` | Target memory utilisation percentage for autoscaling                | `null`                                       |
| `nodeSelector`                                  | Node labels for pod assignment                                      | `{}`                                         |
| `tolerations`                                   | Toleration labels for pod assignment                                | `[]`                                         |
| `updateStrategy`                                | Configure deployment update strategy                                | `{}` (defaults to `RollingUpdate`)           |
| `affinity`                                      | Affinity settings for pod assignment                                | `{}`                                         |
| `extraEnvs`                                     | Additional environment variables to set in the NetBox container     | `[]`                                         |
| `extraVolumeMounts`                             | Additional volumes to mount in the NetBox container                 | `[]`                                         |
| `extraVolumes`                                  | Additional volumes to reference in pods                             | `[]`                                         |
| `extraContainers`                               | Additional sidecar containers to be added to pods                   | `[]`                                         |
| `extraInitContainers`                           | Additional init containers to run before starting main containers   | `[]`                                         |
| `worker`                                        | Worker specific variables. Most global variables also apply here.   | *see `values.yaml`*                          |
| `housekeeping.enabled`                          | Whether the [Housekeeping][housekeeping] `CronJob` should be active | `true`                                       |
| `housekeeping.concurrencyPolicy`                | ConcurrencyPolicy for the Housekeeping CronJob.                     | `Forbid`                                     |
| `housekeeping.failedJobsHistoryLimit`           | Number of failed jobs to keep in history                            | `5`                                          |
| `housekeeping.restartPolicy`                    | Restart Policy for the Housekeeping CronJob.                        | `OnFailure`                                  |
| `housekeeping.schedule`                         | Schedule for the CronJob in [Cron syntax][cron syntax].             | `0 0 * * *` (Midnight daily)                 |
| `housekeeping.successfulJobsHistoryLimit`       | Number of successful jobs to keep in history                        | `5`                                          |
| `housekeeping.suspend`                          | Whether to suspend the CronJob                                      | `false`                                      |
| `housekeeping.podAnnotations`                   | Additional annotations for housekeeping CronJob pods                | `{}`                                         |
| `housekeeping.podLabels`                        | Additional labels for housekeeping CronJob pods                     | `{}`                                         |
| `housekeeping.podSecurityContext`               | Security context for housekeeping CronJob pods                      | *see `values.yaml`*                          |
| `housekeeping.securityContext`                  | Security context for housekeeping CronJob containers                | *see `values.yaml`*                          |
| `housekeeping.automountServiceAccountToken`     | Whether to automatically mount the serviceAccount token in the housekeeping container or not | `false`             |
| `housekeeping.resources`                        | Configure resource requests or limits for housekeeping CronJob      | `{}`                                         |
| `housekeeping.nodeSelector`                     | Node labels for housekeeping CronJob pod assignment                 | `{}`                                         |
| `housekeeping.tolerations`                      | Toleration labels for housekeeping CronJob pod assignment           | `[]`                                         |
| `housekeeping.affinity`                         | Affinity settings for housekeeping CronJob pod assignment           | `{}`                                         |
| `housekeeping.extraEnvs`                        | Additional environment variables to set in housekeeping CronJob     | `[]`                                         |
| `housekeeping.extraVolumeMounts`                | Additional volumes to mount in the housekeeping CronJob             | `[]`                                         |
| `housekeeping.extraVolumes`                     | Additional volumes to reference in housekeeping CronJob pods        | `[]`                                         |
| `housekeeping.extraContainers`                  | Additional sidecar containers to be added to housekeeping CronJob   | `[]`                                         |
| `housekeeping.extraInitContainers`              | Additional init containers for housekeeping CronJob pods            | `[]`                                         |

[netbox-docker startup scripts]: https://github.com/netbox-community/netbox-docker/tree/master/startup_scripts
[CORS]: https://github.com/ottoyiu/django-cors-headers
[housekeeping]: https://demo.netbox.dev/static/docs/administration/housekeeping/
[cron syntax]: https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install` or provide a YAML file containing the values for the above parameters:

```shell
$ helm install --name my-release bootc/netbox --values values.yaml
```

## Persistent storage pitfalls

Persistent storage for media is enabled by default, but unless you take special
care you will run into issues. The most common issue is that one of the NetBox
pods gets stuck in the `ContainerCreating` state. There are several ways around
this problem:

1. For production usage I recommend **disabling** persistent storage by setting
   `persistence.enabled` to `false` and using the S3 `storageBackend`. This can
   be used with any S3-compatible storage provider including Amazon S3, Minio,
   Ceph RGW, and many others. See further down for an example of this.
2. Use a `ReadWriteMany` volume that can be mounted by several pods across
   nodes simultaneously.
3. Configure pod affinity settings to keep all the pods on the same node. This
   allows a `ReadWriteOnce` volume to be mounted in several pods at the same
   time.
4. Disable persistent storage of media altogether and just manage without. The
   storage functionality is only needed to store uploaded image attachments.

To configure the pod affinity to allow using a `ReadWriteOnce` volume you can
use the following example configuration:

```yaml
affinity:
  podAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app.kubernetes.io/name: netbox
      topologyKey: kubernetes.io/hostname


housekeeping:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app.kubernetes.io/name: netbox
        topologyKey: kubernetes.io/hostname

worker:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app.kubernetes.io/name: netbox
        topologyKey: kubernetes.io/hostname
```

## Using an Existing Secret

Rather than specifying passwords and secrets as part of the Helm release values,
you may pass these to NetBox using a pre-existing `Secret` resource. When using
this, the `Secret` must contain the following keys:

| Key                    | Description                                                   | Required?                                                                                         |
| -----------------------|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `db_password`          | The password for the external PostgreSQL database             | If `postgresql.enabled` is `false` and `externalDatabase.existingSecretName` is unset             |
| `email_password`       | SMTP user password                                            | Yes, but the value may be left blank if not required                                              |
| `ldap_bind_password`   | Password for LDAP bind DN                                     | If `remoteAuth.enabled` is `true` and `remoteAuth.backend` is `netbox.authentication.LDAPBackend` |
| `redis_tasks_password` | Password for the external Redis tasks database                | If `redis.enabled` is `false` and `tasksRedis.existingSecretName` is unset                        |
| `redis_cache_password` | Password for the external Redis cache database                | If `redis.enabled` is `false` and `cachingRedis.existingSecretName` is unset                      |
| `secret_key`           | Django secret key used for sessions and password reset tokens | Yes                                                                                               |
| `superuser_password`   | Password for the initial super-user account                   | Yes                                                                                               |
| `superuser_api_token`  | API token created for the initial super-user account          | Yes                                                                                               |

## Using extraConfig for S3 storage configuration

If you want to use S3 as your storage backend and not have the config in the `values.yaml` (credentials!)
you can use an existing secret that is then referenced under the `extraConfig` key.

The secret would look like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  labels:
    app.kubernetes.io/instance: netbox
  name: netbox-extra
stringData:
  s3-config.yaml: |
    STORAGE_CONFIG:
      AWS_S3_ENDPOINT_URL: <endpoint-URL>
      AWS_S3_REGION_NAME: <region>
      AWS_STORAGE_BUCKET_NAME: <bucket-name>
      AWS_ACCESS_KEY_ID: <access-key>
      AWS_SECRET_ACCESS_KEY: <secret-key>
```

And the secret then has to be referenced like this:

```yaml
extraConfig:
  - secret: # same as pod.spec.volumes.secret
      secretName: netbox-extra
```

## Authentication
* [Single Sign On](docs/auth.md#configuring-sso)
* [LDAP Authentication](docs/auth.md#using-ldap-authentication)

## License

> The following notice applies to all files contained within this Helm Chart and
> the Git repository which contains it:
>
> Copyright 2019-2020 Chris Boot
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
>     http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.
