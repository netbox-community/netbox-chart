# NetBox Operator

[Operator](https://github.com/netbox-community/netbox-operator) to manage [NetBox](https://netbox.dev) resources directly through Kubernetes.

## TL;DR

```shell
helm install netbox-operator oci://ghcr.io/netbox-community/netbox-chart/netbox-operator
```

## Prerequisites

- Kubernetes [1.25+](https://kubernetes.io/releases/)
- Helm [3.10+](https://helm.sh/docs/topics/version_skew/)
- NetBox [4.0+](https://netboxlabs.com/docs/netbox/en/stable/release-notes/)

> [!warning]
> NetBox Operator requires additional NetBox configuration.
> A custom field (by default `netboxOperatorRestorationHash`) must be added before operator installation.

## Installing the Chart

To install the chart with the release name `my-release` and default configuration:

```shell
helm install my-release oci://ghcr.io/netbox-community/netbox-chart/netbox-operator
```

## Configuration

The configurable parameters for this chart and their default values are listed on the [`values.yaml`](./values.yaml) file.

## License

This project is licensed under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
