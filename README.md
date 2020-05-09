# NetBox

[NetBox](https://netbox.readthedocs.io/) is an IP address management (IPAM) and
data center infrastructure management (DCIM) tool.

## TL;DR

```shell
$ helm repo add bootc https://charts.boo.tc
$ helm install bootc/netbox
```

## Prerequisites

- This chart has only been tested on Kubernetes 1.12+, but should work on older versions
- This chart works with NetBox 2.7.11+
- Recent versions of Helm 2 or 3 are supported

## Installing the Chart

To install the chart with the release name `my-release` and default configuration:

```shell
$ helm repo add bootc https://charts.boo.tc
$ helm install --name my-release bootc/netbox
```

The default configuration includes the required PostgreSQL and Redis database
services, but either or both may be managed externally if required.

## Uninstalling the Chart

To delete the chart:

```shell
$ helm delete my-release
```

## Upgrading

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

| Parameter                             | Description                                                         | Default                                      |
| --------------------------------------|---------------------------------------------------------------------|----------------------------------------------|
| `replicaCount`                        | The desired number of NetBox pods                                   | `1`                                          |
| `image.repository`                    | NetBox container image repository                                   | `netboxcommunity/netbox`                     |
| `image.tag`                           | NetBox container image tag                                          | `v2.8.3`                                     |
| `image.pullPolicy`                    | NetBox container image pull policy                                  | `IfNotPresent`                               |
| `superuser.name`                      | Initial super-user account to create                                | `admin`                                      |
| `superuser.email`                     | Email address for the initial super-user account                    | `admin@example.com`                          |
| `superuser.password`                  | Password for the initial super-user account                         | `admin`                                      |
| `superuser.apiToken`                  | API token created for the initial super-user account                | `0123456789abcdef0123456789abcdef01234567`   |
| `skipStartupScripts`                  | Skip [netbox-docker startup scripts]                                | `true`                                       |
| `allowedHosts`                        | List of valid FQDNs for this NetBox instance                        | `["*"]`                                      |
| `admins`                              | List of admins to email about critical errors                       | `[]`                                         |
| `banner.top`                          | Banner text to display at the top of every page                     | `""`                                         |
| `banner.bottom`                       | Banner text to display at the bottom of every page                  | `""`                                         |
| `banner.login`                        | Banner text to display on the login page                            | `""`                                         |
| `basePath`                            | Base URL path if accessing NetBox within a directory                | `""`                                         |
| `cacheTimeout`                        | Cached object time-to-live, in seconds                              | `900` (15 minutes)                           |
| `changelogRetention`                  | Maximum number of days to retain logged changes (0 = forever)       | `90`                                         |
| `cors.originAllowAll`                 | [CORS]: allow all origins                                           | `false`                                      |
| `cors.originWhitelist`                | [CORS]: list of origins authorised to make cross-site HTTP requests | `[]`                                         |
| `cors.originRegexWhitelist`           | [CORS]: list of regex strings matching authorised origins           | `[]`                                         |
| `debug`                               | Enable NetBox debugging (NOT for production use)                    | `false`                                      |
| `email.server`                        | SMTP server to use to send emails                                   | `localhost`                                  |
| `email.port`                          | TCP port to connect to the SMTP server on                           | `25`                                         |
| `email.username`                      | Optional username for SMTP authentication                           | `""`                                         |
| `email.password`                      | Password for SMTP authentication (see also `existingSecret`)        | `""`                                         |
| `email.timeout`                       | Timeout for SMTP connections, in seconds                            | `10`                                         |
| `email.from`                          | Sender address for emails sent by NetBox                            | `""`                                         |
| `enforceGlobalUnique`                 | Enforce unique IP space in the global table (not in a VRF)          | `false`                                      |
| `exemptViewPermissions`               | A list of models to exempt from the enforcement of view permissions | `[]`                                         |
| `logging`                             | Custom Django logging configuration                                 | `{}`                                         |
| `loginRequired`                       | Permit only logged-in users to access NetBox                        | `false` (unauthenticated read-only access)   |
| `maintenanceMode`                     | Display a "maintenance mode" banner on every page                   | `false`                                      |
| `maxPageSize`                         | Maximum number of objects that can be returned by a single API call | `1000`                                       |
| `napalm.username`                     | Username used by the NAPALM library to access network devices       | `""`                                         |
| `napalm.password`                     | Password used by the NAPALM library (see also `existingSecret`)     | `""`                                         |
| `napalm.timeout`                      | Timeout for NAPALM to connect to a device (in seconds)              | `30`                                         |
| `napalm.args`                         | A dictionary of optional arguments to pass to NAPALM                | `{}`                                         |
| `paginateCount`                       | The default number of objects to display per page in the web UI     | `50`                                         |
| `plugins`                             | Additional plugins to load into NetBox                              | `[]`                                         |
| `pluginsConfig`                       | Configuration for the additional plugins                            | `{}`                                         |
| `preferIPv4`                          | Prefer devices' IPv4 address when determining their primary address | `false`                                      |
| `remoteAuth.enabled`                  | Enable remote authentication support                                | `false`                                      |
| `remoteAuth.backend`                  | Remote authentication backend class                                 | `utilities.auth_backends.RemoteUserBackend`  |
| `remoteAuth.header`                   | The name of the HTTP header which conveys the username              | `HTTP_REMOTE_USER`                           |
| `remoteAuth.autoCreateUser`           | Enables the automatic creation of new users                         | `true`                                       |
| `remoteAuth.defaultGroups`            | A list of groups to assign to newly created users                   | `[]`                                         |
| `remoteAuth.defaultPermissions`       | A list of permissions to assign newly created users                 | `[]`                                         |
| `releaseCheck.timeout`                | How often NetBox queries GitHub for new releases, if enabled        | `86400`                                      |
| `releaseCheck.url`                    | Release check URL (GitHub API URL; see `values.yaml`)               | `null` (disabled by default)                 |
| `metricsEnabled`                      | Expose Prometheus metrics at the `/metrics` HTTP endpoint           | `false`                                      |
| `timeZone`                            | The time zone NetBox will use when dealing with dates and times     | `UTC`                                        |
| `dateFormat`                          | Django date format for long-form date strings                       | `"N j, Y"`                                   |
| `shortDateFormat`                     | Django date format for short-form date strings                      | `"Y-m-d"`                                    |
| `timeFormat`                          | Django date format for long-form time strings                       | `"g:i a"`                                    |
| `shortTimeFormat`                     | Django date format for short-form time strings                      | `"H:i:s"`                                    |
| `dateTimeFormat`                      | Django date format for long-form date and time strings              | `"N j, Y g:i a"`                             |
| `shortDateTimeFormat`                 | Django date format for short-form date and time strongs             | `"Y-m-d H:i"`                                |
| `secretKey`                           | Django secret key used for sessions and password reset tokens       | `""` (generated)                             |
| `existingSecret`                      | Use an existing Kubernetes `Secret` for secret values (see below)   | `""` (use individual chart values)           |
| `postgresql.enabled`                  | Deploy PostgreSQL using bundled Bitnami PostgreSQL chart            | `true`                                       |
| `postgresql.postgresqlUsername`       | Username to create for NetBox in bundled PostgreSQL instance        | `netbox`                                     |
| `postgresql.postgresqlDatabase`       | Databaes to create for NetBox in bundled PostgreSQL instance        | `netbox`                                     |
| `postgresql.*`                        | Values under this key are passed to the bundled PostgreSQL chart    | n/a                                          |
| `externalDatabase.host`               | PostgreSQL host to use when `postgresql.enabled` is `false`         | `localhost`                                  |
| `externalDatabase.port`               | Port number for external PostgreSQL                                 | `5432`                                       |
| `externalDatabase.database`           | Database name for external PostgreSQL                               | `netbox`                                     |
| `externalDatabase.username`           | Username for external PostgreSQL                                    | `netbox`                                     |
| `externalDatabase.password`           | Password for external PostgreSQL (see also `existingSecret`)        | `""`                                         |
| `externalDatabase.existingSecretName` | Fetch password for external PostgreSQL from a different `Secret`    | `""`                                         |
| `externalDatabase.existingSecretKey`  | Key to fetch the password in the above `Secret`                     | `postgresql-password`                        |
| `redis.enabled`                       | Deploy Redis using bundled Bitnami Redis chart                      | `true`                                       |
| `redis.*`                             | Values under this key are passed to the bundled Redis chart         | n/a                                          |
| `webhooksRedis.database`              | Redis database number used for NetBox webhooks queue                | `0`                                          |
| `webhooksRedis.timeout`               | Redis connection timeout, in seconds                                | `300` (5 minutes)                            |
| `webhooksRedis.ssl`                   | Enable SSL when connecting to Redis                                 | `false`                                      |
| `webhooksRedis.host`                  | Redis host to use when `redis.enabled` is `false`                   | `"netbox-redis"`                             |
| `webhooksRedis.port`                  | Port number for external Redis                                      | `6379`                                       |
| `webhooksRedis.sentinels`             | List of sentinels in `host:port` form (`host` and `port` not used)  | `[]`                                         |
| `webhooksRedis.sentinelService`       | Sentinel master service name                                        | `"netbox-redis"`                             |
| `webhooksRedis.password`              | Password for external Redis (see also `existingSecret`)             | `""`                                         |
| `webhooksRedis.existingSecretName`    | Fetch password for external Redis from a different `Secret`         | `""`                                         |
| `webhooksRedis.existingSecretKey`     | Key to fetch the password in the above `Secret`                     | `redis-password`                             |
| `cachingRedis.database`               | Redis database number used for caching views                        | `1`                                          |
| `cachingRedis.timeout`                | Redis connection timeout, in seconds                                | `300` (5 minutes)                            |
| `cachingRedis.ssl`                    | Enable SSL when connecting to Redis                                 | `false`                                      |
| `cachingRedis.host`                   | Redis host to use when `redis.enabled` is `false`                   | `"netbox-redis"`                             |
| `cachingRedis.port`                   | Port number for external Redis                                      | `6379`                                       |
| `cachingRedis.sentinels`              | List of sentinels in `host:port` form (`host` and `port` not used)  | `[]`                                         |
| `cachingRedis.sentinelService`        | Sentinel master service name                                        | `"netbox-redis"`                             |
| `cachingRedis.password`               | Password for external Redis (see also `existingSecret`)             | `""`                                         |
| `cachingRedis.existingSecretName`     | Fetch password for external Redis from a different `Secret`         | `""`                                         |
| `cachingRedis.existingSecretKey`      | Key to fetch the password in the above `Secret`                     | `redis-password`                             |
| `imagePullSecrets`                    | List of `Secret` names containing private registry credentials      | `[]`                                         |
| `nameOverride`                        | Override the application name (`netbox`) used throughout the chart  | `""`                                         |
| `fullnameOverride`                    | Override the full name of resources created as part of the release  | `""`                                         |
| `persistence.enabled`                 | Enable storage persistence for uploaded media (images)              | `true`                                       |
| `persistence.existingClaim`           | Use an existing `PersistentVolumeClaim` instead of creating one     | `""`                                         |
| `persistence.subPath`                 | Mount a sub-path of the volume into the container, not the root     | `""`                                         |
| `persistence.storageClass`            | Set the storage class of the PVC (use `-` to disable provisioning)  | `""`                                         |
| `persistence.accessMode`              | Access mode for the volume                                          | `ReadWriteOnce`                              |
| `persistence.size`                    | Size of persistent volume to request                                | `1Gi`                                        |
| `reportsPersistence.enabled`          | Enable storage persistence for NetBox reports                       | `false`                                      |
| `reportsPersistence.existingClaim`    | Use an existing `PersistentVolumeClaim` instead of creating one     | `""`                                         |
| `reportsPersistence.subPath`          | Mount a sub-path of the volume into the container, not the root     | `""`                                         |
| `reportsPersistence.storageClass`     | Set the storage class of the PVC (use `-` to disable provisioning)  | `""`                                         |
| `reportsPersistence.accessMode`       | Access mode for the volume                                          | `ReadWriteOnce`                              |
| `reportsPersistence.size`             | Size of persistent volume to request                                | `1Gi`                                        |
| `service.type`                        | Type of `Service` resource to create                                | `ClusterIP`                                  |
| `service.port`                        | Port number for the service                                         | `80`                                         |
| `service.loadBalancerSourceRanges`    | A list of allowed IP ranges when `service.type` is LoadBalancer     | `[]`                                         |
| `ingress.enabled`                     | Create an `Ingress` resource for accessing NetBox                   | `false`                                      |
| `ingress.annotations`                 | Extra annotations to apply to the `Ingress` resource                | `{}`                                         |
| `ingress.hosts`                       | List of hosts and paths to map to the service (see `values.yaml`)   | `[{host:"chart-example.local",paths:["/"]}]` |
| `ingress.tls`                         | TLS settings for the `Ingress` resource                             | `[]`                                         |
| `resources`                           | Configure resource requests or limits for NetBox                    | `{}`                                         |
| `nginx.image.repository`              | NGINX container image repository for proxy and static file serving  | `nginx`                                      |
| `nginx.image.tag`                     | NGINX container image tag                                           | `1.16.0-alpine`                              |
| `nginx.image.pullPolicy`              | NGINX container image pull policy                                   | `IfNotPresent`                               |
| `nginx.resources`                     | Configure resource requests or limits for NGINX                     | `{}`                                         |
| `podAnnotations`                      | Additional annotations for NetBox pods                              | `{}`                                         |
| `nodeSelector`                        | Node labels for pod assignment                                      | `{}`                                         |
| `tolerations`                         | Toleration labels for pod assignment                                | `[]`                                         |
| `updateStrategy`                      | Configure deployment update strategy                                | `{}` (defaults to `RollingUpdate`)           |
| `affinity`                            | Affinity settings for pod assignment                                | `{}`                                         |
| `extraEnvs`                           | Additional environment variables to set in the NetBox container     | `[]`                                         |
| `extraVolumeMounts`                   | Additional volumes to mount in the NetBox container                 | `[]`                                         |
| `extraVolumes`                        | Additional volumes to reference in pods                             | `[]`                                         |
| `extraContainers`                     | Additional sidecar containers to be added to pods                   | `[]`                                         |
| `extraInitContainers`                 | Additional init containers to run before starting main containers   | `[]`                                         |

[netbox-docker startup scripts]: https://github.com/netbox-community/netbox-docker/tree/master/startup_scripts
[CORS]: https://github.com/ottoyiu/django-cors-headers

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
| `redis_password`       | Password for the external Redis tasks database         | If `redis.enabled` is `false` and `webhooksRedis.existingSecretName` is unset         |
| `redis_cache_password` | Password for the external Redis cache database         | If `redis.enabled` is `false` and `cachingRedis.existingSecretName` is unset          |
| `secret_key`           | Django session and password reset token encryption key | Yes, and should be 50+ random characters                                              |
