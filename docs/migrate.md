# Migrating from bootc/netbox-chart & NetBox version 3.2.8 to netbox-community/netbox-chart with the latest version

This doc explains how to migrate from the older bootc/netbox-chart with NetBox version 3.2.8 and bundled Postgres 11 to the official chart, netbox-community/netbox-chart with the latest version and using an external Postgres instance instead. 

1. Backup database:
	1. Attach to the PostgreSQL pod and dump the database
	2. `pg_dump --format=custom -cU postgres -d "dbname=netbox" > /bitnami/postgresql/netbox.sql`
2. Then I manually update the NetBox image tag to version 3.5.9 as this is the latest version that supports Postgres 11
	1. For this migration to run succesfully I had to provide env variable "NETBOX_DELETE_LEGACY_DATA" and set the value to 1 
3. Restore the database dump into the external Postgres 12 database (In my case I use the Postgres Operator to manage this)
	1. `pg_restore -v -Fc -c -U netbox -d netbox < /bitnami/postgresql/netbox.sql`
4. Once running on 3.5.9 I changed the database connection to the externally running Postgres 12 database and restarted NetBox and let all the migrations run as normal
5. Once running I started upgrading NetBox further (Still by updating the image tag) going the recommended version increments of:
	1. 3.5.9 > 3.6.9
	2. 3.6.9 > 3.7.8
	3. 3.7.8 > 4.0.2
	4. 4.0.2 > To the latest version
	5. Make sure to let the migration finish on each increment. Check https://netboxlabs.com/docs/netbox/en/stable/installation/upgrading/ for more details
6. Once running on a 4.x.x version it was time to switch over to using the new and official chart: oci://ghcr.io/netbox-community/netbox-chart/netbox 
	1. In my case, using ArgoCD this did not work so I had to use the https version, more details regarding this can be seen here: https://github.com/netbox-community/netbox-chart/issues/252
7. Once NetBox is running by being deployed from this chart I had to fix a few things:
	1. In the Redis chart values.yaml I had to update the 'clusterDomain' parameter (Only applicable if you are using the non default one, e.g **not** cluster.local)
	2. The remoteAuth backend parameters changed slightly and is now in a list format instead (Only applicable if using remoteAuth)
    3. Optional, but I also upgraded Postgres from v12 to v16 without any problems  