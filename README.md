# NetBox

[NetBox](https://netbox.readthedocs.io/) is an IP address management (IPAM) and
data center infrastructure management (DCIM) tool.

## TL;DR

```shell
$ helm repo add bootc https://charts.boo.tc
$ helm install netbox \
  --set postgresql.postgresqlPostgresPassword=[password1] \
  --set postgresql.postgresqlPassword=[password2] \
  --set redis.auth.password=[password3] \
  bootc/netbox
```

## Prerequisites

- This chart has only been tested on Kubernetes 1.18+, but should work on 1.14+
- This chart works with NetBox 2.10.4+
- Recent versions of Helm 3 are supported

## Installing the Chart

To install the chart with the release name `my-release` and default configuration:

```shell
$ helm repo add bootc https://charts.boo.tc
$ helm install my-release \
  --set postgresql.postgresqlPostgresPassword=[password1] \
  --set postgresql.postgresqlPassword=[password2] \
  --set redis.auth.password=[password3] \
  bootc/netbox
```

The default configuration includes the required PostgreSQL and Redis database
services, but either or both may be managed externally if required.

## Uninstalling the Chart

To delete the chart:

```shell
$ helm delete my-release
```

## Upgrading

### Bundled PostgreSQL

When upgrading or changing settings and using the bundled Bitnami PostgreSQL
sub-chart, you **must** provide the `postgresql.postgresqlPassword` at minimum.
Ideally you should also upply the `postgresql.postgresqlPostgresPassword` and,
if using replication, the `postgresql.replication.password`. Please see the
[upstream documentation](https://github.com/bitnami/charts/tree/master/bitnami/postgresql#upgrading)
for further information.

### From 3.x to 4.x

* The Bitnami [Redis](https://github.com/bitnami/charts/tree/master/bitnami/redis) sub-chart was upgraded from 12.x to 15.x; please read the upstream upgrade notes if you are using the bundled Redis

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
| `superuser.name`                                | Initial super-user account to create                                | `admin`                                      |
| `superuser.email`                               | Email address for the initial super-user account                    | `admin@example.com`                          |
| `superuser.password`                            | Password for the initial super-user account                         | `admin`                                      |
| `superuser.apiToken`                            | API token created for the initial super-user account                | `0123456789abcdef0123456789abcdef01234567`   |
| `skipStartupScripts`                            | Skip [netbox-docker startup scripts]                                | `true`                                       |
| `allowedHosts`                                  | List of valid FQDNs for this NetBox instance                        | `["*"]`                                      |
| `admins`                                        | List of admins to email about critical errors                       | `[]`                                         |
| `allowedUrlSchemes`                             | URL schemes that are allowed within links in NetBox                 | *see `values.yaml`*                          |
| `banner.top`                                    | Banner text to display at the top of every page                     | `""`                                         |
| `banner.bottom`                                 | Banner text to display at the bottom of every page                  | `""`                                         |
| `banner.login`                                  | Banner text to display on the login page                            | `""`                                         |
| `basePath`                                      | Base URL path if accessing NetBox within a directory                | `""`                                         |
| `cacheTimeout`                                  | Cached object time-to-live, in seconds                              | `900` (15 minutes)                           |
| `changelogRetention`                            | Maximum number of days to retain logged changes (0 = forever)       | `90`                                         |
| `cors.originAllowAll`                           | [CORS]: allow all origins                                           | `false`                                      |
| `cors.originWhitelist`                          | [CORS]: list of origins authorised to make cross-site HTTP requests | `[]`                                         |
| `cors.originRegexWhitelist`                     | [CORS]: list of regex strings matching authorised origins           | `[]`                                         |
| `debug`                                         | Enable NetBox debugging (NOT for production use)                    | `false`                                      |
| `email.server`                                  | SMTP server to use to send emails                                   | `localhost`                                  |
| `email.port`                                    | TCP port to connect to the SMTP server on                           | `25`                                         |
| `email.username`                                | Optional username for SMTP authentication                           | `""`                                         |
| `email.password`                                | Password for SMTP authentication (see also `existingSecret`)        | `""`                                         |
| `email.useSSL`                                  | Use SSL when connecting to the server                               | `false`                                      |
| `email.useTLS`                                  | Use TLS when connecting to the server                               | `false`                                      |
| `email.timeout`                                 | Timeout for SMTP connections, in seconds                            | `10`                                         |
| `email.from`                                    | Sender address for emails sent by NetBox                            | `""`                                         |
| `enforceGlobalUnique`                           | Enforce unique IP space in the global table (not in a VRF)          | `false`                                      |
| `exemptViewPermissions`                         | A list of models to exempt from the enforcement of view permissions | `[]`                                         |
| `httpProxies`                                   | HTTP proxies NetBox should use when sending outbound HTTP requests  | `null`                                       |
| `internalIPs`                                   | IP addresses recognized as internal to the system                   | `['127.0.0.1', '::1']`                       |
| `logging`                                       | Custom Django logging configuration                                 | `{}`                                         |
| `loginRequired`                                 | Permit only logged-in users to access NetBox                        | `false` (unauthenticated read-only access)   |
| `loginTimeout`                                  | How often to re-authenticate users                                  | `1209600` (14 days)                          |
| `maintenanceMode`                               | Display a "maintenance mode" banner on every page                   | `false`                                      |
| `mapsUrl`                                       | The URL to use when mapping physical addresses or GPS coordinates   | `https://maps.google.com/?q=`                |
| `maxPageSize`                                   | Maximum number of objects that can be returned by a single API call | `1000`                                       |
| `storageBackend`                                | Django-storages backend class name                                  | `null`                                       |
| `storageConfig`                                 | Django-storages backend configuration                               | `{}`                                         |
| `metricsEnabled`                                | Expose Prometheus metrics at the `/metrics` HTTP endpoint           | `false`                                      |
| `napalm.username`                               | Username used by the NAPALM library to access network devices       | `""`                                         |
| `napalm.password`                               | Password used by the NAPALM library (see also `existingSecret`)     | `""`                                         |
| `napalm.timeout`                                | Timeout for NAPALM to connect to a device (in seconds)              | `30`                                         |
| `napalm.args`                                   | A dictionary of optional arguments to pass to NAPALM                | `{}`                                         |
| `paginateCount`                                 | The default number of objects to display per page in the web UI     | `50`                                         |
| `plugins`                                       | Additional plugins to load into NetBox                              | `[]`                                         |
| `pluginsConfig`                                 | Configuration for the additional plugins                            | `{}`                                         |
| `preferIPv4`                                    | Prefer devices' IPv4 address when determining their primary address | `false`                                      |
| `rackElevationDefaultUnitHeight`                | Rack elevation default height in pixels                             | `22`                                         |
| `rackElevationDefaultUnitWidth`                 | Rack elevation default width in pixels                              | `220`                                        |
| `remoteAuth.enabled`                            | Enable remote authentication support                                | `false`                                      |
| `remoteAuth.backend`                            | Remote authentication backend class                                 | `netbox.authentication.RemoteUserBackend`    |
| `remoteAuth.header`                             | The name of the HTTP header which conveys the username              | `HTTP_REMOTE_USER`                           |
| `remoteAuth.autoCreateUser`                     | Enables the automatic creation of new users                         | `true`                                       |
| `remoteAuth.defaultGroups`                      | A list of groups to assign to newly created users                   | `[]`                                         |
| `remoteAuth.defaultPermissions`                 | A list of permissions to assign newly created users                 | `{}`                                         |
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
| `releaseCheck.timeout`                          | How often NetBox queries GitHub for new releases, if enabled        | `86400`                                      |
| `releaseCheck.url`                              | Release check URL (GitHub API URL; see `values.yaml`)               | `null` (disabled by default)                 |
| `timeZone`                                      | The time zone NetBox will use when dealing with dates and times     | `UTC`                                        |
| `dateFormat`                                    | Django date format for long-form date strings                       | `"N j, Y"`                                   |
| `shortDateFormat`                               | Django date format for short-form date strings                      | `"Y-m-d"`                                    |
| `timeFormat`                                    | Django date format for long-form time strings                       | `"g:i a"`                                    |
| `shortTimeFormat`                               | Django date format for short-form time strings                      | `"H:i:s"`                                    |
| `dateTimeFormat`                                | Django date format for long-form date and time strings              | `"N j, Y g:i a"`                             |
| `shortDateTimeFormat`                           | Django date format for short-form date and time strongs             | `"Y-m-d H:i"`                                |
| `secretKey`                                     | Django secret key used for sessions and password reset tokens       | `""` (generated)                             |
| `existingSecret`                                | Use an existing Kubernetes `Secret` for secret values (see below)   | `""` (use individual chart values)           |
| `postgresql.enabled`                            | Deploy PostgreSQL using bundled Bitnami PostgreSQL chart            | `true`                                       |
| `postgresql.postgresqlUsername`                 | Username to create for NetBox in bundled PostgreSQL instance        | `netbox`                                     |
| `postgresql.postgresqlDatabase`                 | Database to create for NetBox in bundled PostgreSQL instance        | `netbox`                                     |
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
| `redis.enabled`                                 | Deploy Redis using bundled Bitnami Redis chart                      | `true`                                       |
| `redis.*`                                       | Values under this key are passed to the bundled Redis chart         | n/a                                          |
| `tasksRedis.database`                           | Redis database number used for NetBox task queue                    | `0`                                          |
| `tasksRedis.ssl`                                | Enable SSL when connecting to Redis                                 | `false`                                      |
| `tasksRedis.insecureSkipTlsVerify`              | Skip TLS certificate verification when connecting to Redis          | `false`                                      |
| `tasksRedis.host`                               | Redis host to use when `redis.enabled` is `false`                   | `"netbox-redis"`                             |
| `tasksRedis.port`                               | Port number for external Redis                                      | `6379`                                       |
| `tasksRedis.sentinels`                          | List of sentinels in `host:port` form (`host` and `port` not used)  | `[]`                                         |
| `tasksRedis.sentinelService`                    | Sentinel master service name                                        | `"netbox-redis"`                             |
| `tasksRedis.sentinelTimeout`                    | Sentinel connection timeout, in seconds                             | `300` (5 minutes)                            |
| `tasksRedis.password`                           | Password for external Redis (see also `existingSecret`)             | `""`                                         |
| `tasksRedis.existingSecretName`                 | Fetch password for external Redis from a different `Secret`         | `""`                                         |
| `tasksRedis.existingSecretKey`                  | Key to fetch the password in the above `Secret`                     | `redis-password`                             |
| `cachingRedis.database`                         | Redis database number used for caching views                        | `1`                                          |
| `cachingRedis.ssl`                              | Enable SSL when connecting to Redis                                 | `false`                                      |
| `cachingRedis.insecureSkipTlsVerify`            | Skip TLS certificate verification when connecting to Redis          | `false`                                      |
| `cachingRedis.host`                             | Redis host to use when `redis.enabled` is `false`                   | `"netbox-redis"`                             |
| `cachingRedis.port`                             | Port number for external Redis                                      | `6379`                                       |
| `cachingRedis.sentinels`                        | List of sentinels in `host:port` form (`host` and `port` not used)  | `[]`                                         |
| `cachingRedis.sentinelService`                  | Sentinel master service name                                        | `"netbox-redis"`                             |
| `cachingRedis.sentinelTimeout`                  | Sentinel connection timeout, in seconds                             | `300` (5 minutes)                            |
| `cachingRedis.password`                         | Password for external Redis (see also `existingSecret`)             | `""`                                         |
| `cachingRedis.existingSecretName`               | Fetch password for external Redis from a different `Secret`         | `""`                                         |
| `cachingRedis.existingSecretKey`                | Key to fetch the password in the above `Secret`                     | `redis-password`                             |
| `imagePullSecrets`                              | List of `Secret` names containing private registry credentials      | `[]`                                         |
| `nameOverride`                                  | Override the application name (`netbox`) used throughout the chart  | `""`                                         |
| `fullnameOverride`                              | Override the full name of resources created as part of the release  | `""`                                         |
| `serviceAccount.create`                         | Create a ServiceAccount for NetBox                                  | `true`                                       |
| `serviceAccount.annotations`                    | Annotations to add to the service account                           | `{}`                                         |
| `serviceAccount.name`                           | The name of the service account to use                              | `""` (use the fullname)                      |
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
| `service.loadBalancerSourceRanges`              | A list of allowed IP ranges when `service.type` is LoadBalancer     | `[]`                                         |
| `ingress.enabled`                               | Create an `Ingress` resource for accessing NetBox                   | `false`                                      |
| `ingress.className`                             | Use a named IngressClass                                            | `""`                                         |
| `ingress.annotations`                           | Extra annotations to apply to the `Ingress` resource                | `{}`                                         |
| `ingress.hosts`                                 | List of hosts and paths to map to the service (see `values.yaml`)   | `[{host:"chart-example.local",paths:["/"]}]` |
| `ingress.tls`                                   | TLS settings for the `Ingress` resource                             | `[]`                                         |
| `resources`                                     | Configure resource requests or limits for NetBox                    | `{}`                                         |
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
| `housekeeping.restartPolicy`                    | Restart Policy for the Housekeeping CronJob.                        | `OnFailure`                                  |
| `housekeeping.failedJobsHistoryLimit`           | Number of failed jobs to keep in history                            | `5`                                          |
| `housekeeping.successfulJobsHistoryLimit`       | Number of successful jobs to keep in history                        | `5`                                          |
| `housekeeping.schedule`                         | Schedule for the CronJob in [Cron syntax][cron syntax].             | `0 0 * * *` (Midnight daily)                 |

[netbox-docker startup scripts]: https://github.com/netbox-community/netbox-docker/tree/master/startup_scripts
[CORS]: https://github.com/ottoyiu/django-cors-headers
[housekeeping]: https://demo.netbox.dev/static/docs/administration/housekeeping/
[cron syntax]: https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install` or provide a YAML file containing the values for the above parameters:

```shell
$ helm install --name my-release bootc/netbox --values values.yaml
```

## Using an Existing Secret

Rather than specifying passwords and secrets as part of the Helm release values,
you may pass these to NetBox using a pre-existing `Secret` resource. When using
this, the `Secret` must contain the following keys:

| Key                    | Description                                            | Required? |
| -----------------------|--------------------------------------------------------|---------------------------------------------------------------------------------------|
| `db_password`          | The password for the external PostgreSQL database      | If `postgresql.enabled` is `false` and `externalDatabase.existingSecretName` is unset |
| `email_password`       | SMTP user password                                     | Yes, but the value may be left blank if not required                                  |
| `napalm_password`      | NAPALM user password                                   | Yes, but the value may be left blank if not required                                  |
| `redis_tasks_password` | Password for the external Redis tasks database         | If `redis.enabled` is `false` and `tasksRedis.existingSecretName` is unset            |
| `redis_cache_password` | Password for the external Redis cache database         | If `redis.enabled` is `false` and `cachingRedis.existingSecretName` is unset          |
| `secret_key`           | Django session and password reset token encryption key | Yes, and should be 50+ random characters                                              |

## Using LDAP Authentication

For using LDAP for authentication, specify the ldap-docker image tag of netbox, e.g. "v2.10.3-ldap".

Configuration is done via Helm release values. `remoteAuth` should be enabled and configured for LDAP, e.g.:

```yaml
remoteAuth:
  enabled: true
  backend: 'netbox.authentication.LDAPBackend'
  ldap:
    # see Configuration variables
```

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
