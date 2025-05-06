# Extra Configuration

## Overview

Any additional configuration setting can be passed in the chart
values to be loaded into NetBox's instance.
They may be provided as arbitrary configuration values set, or
you can load arbitrary `*.yaml` keys from ConfigMaps and Secrets.

```yaml
extraConfig:
  - values:
      EXTRA_SETTING_ONE: example
      ANOTHER_SETTING: foobar
  - configMap: # pod.spec.volumes.configMap
      name: netbox-extra
      items: []
      optional: false
  - secret: # same as pod.spec.volumes.secret
      secretName: netbox-extra
      items: []
      optional: false
```

## NetBox Additional Configuration

For additional NetBox configuration setting, the recommended way is
to use the extra configuration value (`extraConfig`).

> [!note]
> In order to keep the chart's values reasonnable, only the 
> [required](https://netboxlabs.com/docs/netbox/en/stable/configuration/required-parameters/) 
> and critical configuration settings can be directly configured with a dedicated value field.

For example, the following snippet is configuring the value for
[`DEFAULT_DASHBOARD`](https://netboxlabs.com/docs/netbox/en/stable/configuration/default-values/#default_dashboard):

```yaml
extraConfig:
  - values:
      DEFAULT_DASHBOARD: 
        - widget: "extras.ObjectCountsWidget"
          width: 4
```

## ConfigMaps and Secrets Use

Any ConfigMaps and Secrets can be leveraged to provide configuration parameters.
The resource must provide the data under a `*.yaml` file description.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: netbox-okta-credentials
  namespace: netbox
type: Opaque
stringData:
  okta.yaml: |
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY: ...
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET: ...
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL: ...
```

Then, it can be consumed using `extraConfig` using a the name as reference.

```yaml
extraConfig:
  - secret:
      secretName: netbox-okta-credentials
```

The variables will be retrieve by NetBox when loading.
In this example, the three variables (`SOCIAL_AUTH_OKTA_OPENIDCONNECT_*`)
will be available as global variables.

> [!tip]
> See more example of `extraConfig` within [Authentication Options](./auth.md) guide.
