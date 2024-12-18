# Migration Guide

For major version updates (5.0.0, 6.0.0, etc.), see the release notes for detailed migration information.

## Back Up PostgreSQL

The first thing you should do is back up your PostgreSQL database.
This way you can always go back to your previous install version if anything goes wrong.

You can find your PostgreSQL pod by running `kubectl get pods -A | grep postgres` and then use `kubectl exec` to run `psql` or `pg_dump` from it.

## Upgrade PostgreSQL If Necessary

As of NetBox 3.6.x, NetBox requires PostgreSQL 12 or higher.
It is recommmended that you upgrade to the latest supported PostgreSQL version.

If you are using the built-in PostgreSQL chart, you may need to update it separately, or update to the latest NetBox chart and dump your data back into it before NetBox will start.

## Upgrade NetBox

It is always recommended that you upgrade NetBox one major version at a time.
For example, if you are currently running NetBox 3.5.2 inside your chart, you would upgrade to the last 3.6.x version, then 3.7.x, and so on.

This ensures that migrations all run smoothly between versions.

## Check for Breaking Changes

Always look at the release notes for breaking changes.
There may be necessary changes to your `values.yaml` to ensure your configuration still works.
