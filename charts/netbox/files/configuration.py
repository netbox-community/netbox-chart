"""
This file serves as a base configuration for Netbox
https://netboxlabs.com/docs/netbox/en/stable/configuration/
"""

import os
import re
from pathlib import Path

import yaml


def _deep_merge(source, destination):
    """Inspired by https://stackoverflow.com/a/20666342"""
    for key, value in source.items():
        dst_value = destination.get(key)

        if isinstance(value, dict) and isinstance(dst_value, dict):
            _deep_merge(value, dst_value)
        else:
            destination[key] = value

    return destination


def _load_yaml() -> None:
    """Load YAML from files"""
    extra_config_base = Path("/run/config/extra")
    config_files = [Path("/run/config/netbox/netbox.yaml")]

    config_files.extend(sorted(extra_config_base.glob("*/*.yaml")))

    for config_file in config_files:
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        _deep_merge(config, globals())


def _read_secret(secret_name: str, secret_key: str, default: str | None = None) -> str | None:
    """Read secret from file"""
    try:
        secret = open(
            f"/run/secrets/{secret_name}/{secret_key}",
            "r",
            encoding="utf-8",
        )
    except EnvironmentError:
        return default
    with secret:
        return secret.readline().strip()


CORS_ORIGIN_REGEX_WHITELIST = []
DATABASES = {}
EMAIL = {}
REDIS = {}

_load_yaml()

provided_secret_name = os.getenv("SECRET_NAME", "netbox")

DATABASES["default"]["PASSWORD"] = _read_secret(provided_secret_name, "db_password")
EMAIL["PASSWORD"] = _read_secret(provided_secret_name, "email_password")
REDIS["tasks"]["PASSWORD"] = _read_secret(provided_secret_name, "tasks_password")
REDIS["caching"]["PASSWORD"] = _read_secret(provided_secret_name, "cache_password")
SECRET_KEY = _read_secret(provided_secret_name, "secret_key")

# Post-process certain values
CORS_ORIGIN_REGEX_WHITELIST = [re.compile(r) for r in CORS_ORIGIN_REGEX_WHITELIST]
if "SENTINELS" in REDIS["tasks"]:
    REDIS["tasks"]["SENTINELS"] = [tuple(x.split(r":")) for x in REDIS["tasks"]["SENTINELS"]]
if "SENTINELS" in REDIS["caching"]:
    REDIS["caching"]["SENTINELS"] = [tuple(x.split(r":")) for x in REDIS["caching"]["SENTINELS"]]
if ALLOWED_HOSTS_INCLUDES_POD_ID:
    ALLOWED_HOSTS.append(os.getenv("POD_IP"))
