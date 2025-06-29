"""
Gandi Dynamic DNS 1.3

Dynamic DNS Update Client for Gandi's LiveDNS

Copyright (C) 2025 Winston Astrachan
Released under the terms of the MIT license
"""

import os
from typing import Any, Dict, Optional, Tuple, Union

import requests

CACHE_KEY_IPV4 = "/run/ipv4.last"
CACHE_KEY_IPV6 = "/run/ipv6.last"


def _get_env_var(name: str, default: Any = None, required: bool = False) -> str:
    """Get the value of an environment variable with optional default and required validation.

    Args:
        name: The name of the environment variable to retrieve.
        default: The default value to return if the environment variable is not set.
                 Defaults to None.
        required: Whether the environment variable is required. If True and the
                  environment variable is not set, raises ValueError. Defaults to False.

    Returns:
        The value of the environment variable as a string, or the default value.

    Raises:
        ValueError: If the environment variable is not set and required is True.
    """
    try:
        return os.environ[name]
    except KeyError:
        if required:
            raise ValueError(
                f"The {name} environment variable is required but not set."
            )
        return default


def _get_cache_value(key: str) -> Union[Any, None]:
    """Retrieve a cached value from the filesystem.

    Args:
        key: The cache key (file path) to read from.

    Returns:
        The cached value as a string, or None if the cache file doesn't exist.
    """
    try:
        with open(key) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def _set_cache_value(key: str, value: Any) -> Any:
    """Store a value in the filesystem cache.

    Args:
        key: The cache key (file path) to write to.
        value: The value to store in the cache.

    Returns:
        The value that was stored.
    """
    with open(key, "w") as f:
        f.write(value)
    return value


def _get_headers() -> Dict[str, str]:
    """Build HTTP headers for Gandi API requests.

    Returns:
        A dictionary containing the required HTTP headers for API requests.
    """
    headers = {
        "Content-Type": "application/json",
    }
    if GANDI_KEY:
        headers["Authorization"] = f"Apikey {GANDI_KEY}"
    if GANDI_PAT:
        headers["Authorization"] = f"Bearer {GANDI_PAT}"
    return headers


def get_ipv4() -> Tuple[Optional[str], bool]:
    """Get the current public IPv4 address and check if it has changed.

    Fetches the current public IPv4 address from an external service and compares
    it with the cached value to determine if it has changed.

    Returns:
        A tuple containing:
            - address (str): The current IPv4 address, or None if unavailable.
            - changed (bool): True if the IPv4 address has changed since last check.
    """
    try:
        response = requests.get("https://ipv4.icanhazip.com/")
        response.raise_for_status()
    except Exception:
        address = None
    else:
        address = response.text.strip()
    changed = False
    if address and address != _get_cache_value(CACHE_KEY_IPV4):
        _set_cache_value(CACHE_KEY_IPV4, address)
        changed = True
    return (address, changed)


def get_ipv6() -> Tuple[Optional[str], bool]:
    """Get the current public IPv6 address and check if it has changed.

    Fetches the current public IPv6 address from an external service and compares
    it with the cached value to determine if it has changed.

    Returns:
        A tuple containing:
            - address (str): The current IPv6 address, or None if unavailable.
            - changed (bool): True if the IPv6 address has changed since last check.
    """
    try:
        response = requests.get("https://ipv6.icanhazip.com/")
        response.raise_for_status()
    except Exception:
        address = None
    else:
        address = response.text.strip()
    changed = False
    if address and address != _get_cache_value(CACHE_KEY_IPV6):
        _set_cache_value(CACHE_KEY_IPV6, address)
        changed = True
    return (address, changed)


def update_a_record() -> None:
    """Update the DNS A record if the public IPv4 address has changed.

    Checks the current public IPv4 address and updates the corresponding A record
    in Gandi's DNS service if a change is detected. Prints status messages to
    indicate the result of the operation.
    """
    ip, changed = get_ipv4()
    if not ip:
        print("Unable to fetch current IPV4 address")
    elif changed:
        try:
            payload = {"rrset_values": ["{}".format(ip)]}
            response = requests.put(
                f"{GANDI_URL}domains/{GANDI_DOMAIN}/records/{GANDI_RECORD}/A",
                json=payload,
                headers=_get_headers(),
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Unable to update DNS record: {e}")
        else:
            print(f"Set IP to {ip} for A record '{GANDI_RECORD}' for {GANDI_DOMAIN}")
    else:
        print(f"No change in external IP ({ip}), not updating A record")


def update_aaaa_record() -> None:
    """Update the DNS AAAA record if the public IPv6 address has changed.

    Checks the current public IPv6 address and updates the corresponding AAAA record
    in Gandi's DNS service if a change is detected. Prints status messages to
    indicate the result of the operation.
    """
    ip, changed = get_ipv6()
    if not ip:
        print("Unable to fetch current IPV6 address")
    elif changed:
        try:
            payload = {"rrset_values": ["{}".format(ip)]}
            response = requests.put(
                f"{GANDI_URL}domains/{GANDI_DOMAIN}/records/{GANDI_RECORD}/AAAA",
                json=payload,
                headers=_get_headers(),
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Unable to update DNS record: {e}")
        else:
            print(f"Set IP to {ip} for AAAA record '{GANDI_RECORD}' for {GANDI_DOMAIN}")
    else:
        print("No change in external IP ({ip}), not updating AAAA record")


if __name__ == "__main__":
    GANDI_URL = _get_env_var("GANDI_URL", "https://dns.api.gandi.net/api/v5/")
    GANDI_KEY = _get_env_var("GANDI_KEY")
    GANDI_PAT = _get_env_var("GANDI_PAT")
    GANDI_DOMAIN = _get_env_var("GANDI_DOMAIN", required=True)
    GANDI_RECORD = _get_env_var("GANDI_RECORD", "@")

    # Deprecation checks
    if GANDI_KEY and GANDI_PAT:
        raise ValueError(
            "Both GANDI_KEY and GANDI_PAT are defined. Remove GANDI_KEY from your environment."
        )
    if not GANDI_KEY and not GANDI_PAT:
        raise ValueError("One of GANDI_KEY or GANDI_PAT is required.")
    if GANDI_KEY:
        print(
            "GANDI_KEY is used, but Gandi API keys have been deprecated. Switch to GANDI_PAT."
        )

    # Record updates
    update_a_record()
    update_aaaa_record()
