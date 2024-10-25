# Netbox Helm Charts

> The official [Helm](https://helm.sh) charts repository for [Netbox](https://netbox.dev).

[![Build Status](https://github.com/netbox-community/netbox-chart/actions/workflows/ci.yml/badge.svg)](https://github.com/netbox-community/netbox-chart/actions/workflows/ci.yml)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/netbox)](https://artifacthub.io/packages/search?repo=netbox)

## About

This Git repository houses the official Helm charts for Netbox.

Do you have any questions?
Before opening an issue on GitHub, please join [our Slack](https://join.slack.com/t/netdev-community/shared_invite/zt-mtts8g0n-Sm6Wutn62q_M4OdsaIycrQ)
and ask for help in the [`#netbox-chart`](https://netdev-community.slack.com/archives/C01Q6B100R2) channel.

|                        Chart                        |                                                                                                                    Version                                                                                                                     |
| :-------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|          [`netbox/netbox`](charts/netbox/)          |          [![Chart Version](https://img.shields.io/badge/dynamic/json?label=netbox&query=version&url=https%3A%2F%2Fartifacthub.io%2Fapi%2Fv1%2Fpackages%2Fhelm%2Fnetbox%2Fnetbox)](https://artifacthub.io/packages/helm/netbox/netbox)          |
| [`netbox/netbox-operator`](charts/netbox-operator/) | [![Chart Version](https://img.shields.io/badge/dynamic/json?label=netbox&query=version&url=https%3A%2F%2Fartifacthub.io%2Fapi%2Fv1%2Fpackages%2Fhelm%2Fnetbox%2Fnetbox-operator)](https://artifacthub.io/packages/helm/netbox/netbox-operator) |

## Quickstart

```shell
helm install my-release --devel oci://ghcr.io/netbox-community/netbox-chart/netbox
```

See docs on your preferred sources:

- [Charts docs on Artifact Hub](https://artifacthub.io/packages/search?org=netbox)
- [Charts respective readmes](charts)
- [Charts discovery](https://helm.sh/docs/helm/helm_search/)
  ```sh
  helm search netbox
  ```

## License

This project is licensed under [Apache License, Version 2.0](LICENSE).
