# Production Considerations

## Database Recommendation

We recommend using separate external PostgreSQL and Redis instances. This
de-couples those services from the chart's bundled versions which may have
complex upgrade requirements. A clustered PostgreSQL server (e.g. using Zalando's
[Postgres Operator](https://github.com/zalando/postgres-operator)) and Redis
with Sentinel (e.g. using [Aaron Layfield](https://github.com/DandyDeveloper)'s
[redis-ha chart](https://github.com/DandyDeveloper/charts/tree/master/charts/redis-ha)).


## Storage Recommendation

Set `persistence.enabled` to `false` and use the S3 `storageBackend` and `storageConfig`
for object storage. This works well with Minio or Ceph RGW as well as Amazon S3.
See [Persistent Storage Pitfalls](#persistent-storage-pitfalls), below.

Run multiple replicas of the NetBox web frontend to avoid interruptions during
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

## Persistent Storage Pitfalls

Persistent storage for media is enabled by default, but unless you take special
care you will run into issues. The most common issue is that one of the NetBox
pods gets stuck in the `ContainerCreating` state. There are several ways around
this problem:

<!-- prettier-ignore-start -->

1. Use the recommended S3 `storageBackend` and **disable** persistent storage
    by setting `persistence.enabled` to `false`. This can
    be used with any S3-compatible storage provider including Amazon S3, Minio,
    Ceph RGW, and many others. See further down for an example of this.
2. Use a `ReadWriteMany` volume that can be mounted by several pods across
    nodes simultaneously.
3. Configure pod affinity settings to keep all the pods on the same node. This
    allows a `ReadWriteOnce` volume to be mounted in several pods at the same
    time.
4. Disable persistent storage of media altogether and just manage without. The
    storage functionality is only needed to store uploaded image attachments.

<!-- prettier-ignore-end -->

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
