"""
Gandi Dynamic DNS 1.1

Dynamic DNS Update Client for Gandi's LiveDNS

Copyright (C) 2020 Winston Astrachan
Released under the terms of the MIT license
"""
import os
import requests


CACHE_KEY_IPV4 = '/run/ipv4.last'
CACHE_KEY_IPV6 = '/run/ipv6.last'


def _get_env_var(name, default=None):
    """ Returns value of an environment variable, or a default value.

    Returns:
        - Value of environment variable if environment variable is set
        - Defaut value `default` if environment variable is not set

    Raises:
        ValueError if environment variable is not set AND `default` is False
    """
    try:
        return os.environ[name]
    except KeyError:
        if default is False:
            raise ValueError("The {} environment variable is required but not set.".format(name))
        return default


def _get_cache_value(key):
    """ Returns a value for a cache key, or None """
    address = None
    try:
        with open(key) as f:
            address = f.read()
    except FileNotFoundError:
        address = None
    return address


def _set_cache_value(key, value):
    """ Sets or updates the value for a cache key """
    with open(key, 'w') as f:
        f.seek(0)
        f.write(value)
    return value


def _get_gandi_headers():
    """ Returns API request headers for the Gandi API """
    return {
        'X-Api-Key': GANDI_KEY,
        'Content-Type': 'application/json',
    }


def get_ipv4():
    """ Gets the current public IPV4 address

    Returns:
        (address, changed)
            address: (str) current ipv4 address
            changed: (bool) True if ipv4 address has changed

    """
    try:
        response = requests.get('https://ipv4.icanhazip.com/')
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


def get_ipv6():
    """ Gets the current public IPV6 address

    Returns:
        (address, changed)
            address: (str) current ipv6 address
            changed: (bool) True if ipv6 address has changed

    """
    try:
        response = requests.get('https://ipv6.icanhazip.com/')
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


def update_a_record():
    """ Check public IPV4 address and update A record if a change has occured """
    ip, changed = get_ipv4()
    if not ip:
        print("Unable to fetch current IPV4 address")
    elif changed:
        try:
            payload = {'rrset_values': ['{}'.format(ip)]}
            response = requests.put("{}domains/{}/records/{}/A".format(GANDI_URL, GANDI_DOMAIN, GANDI_RECORD),
                                    json=payload,
                                    headers=_get_gandi_headers())
            response.raise_for_status()
        except Exception as e:
            print("Unable to update DNS record: {}".format(e))
        else:
            print("Set IP to {} for A record '{}' for {}".format(ip, GANDI_RECORD, GANDI_DOMAIN))
    else:
        print("No change in external IP ({}), not updating A record".format(ip))


def update_aaaa_record():
    """ Check public IPV6 address and update AAAA record if a change has occured """
    ip, changed = get_ipv6()
    if not ip:
        print("Unable to fetch current IPV6 address")
    elif changed:
        try:
            payload = {'rrset_values': ['{}'.format(ip)]}
            response = requests.put("{}domains/{}/records/{}/AAAA".format(GANDI_URL, GANDI_DOMAIN, GANDI_RECORD),
                                    json=payload,
                                    headers=_get_gandi_headers())
            response.raise_for_status()
        except Exception as e:
            print("Unable to update DNS record: {}".format(e))
        else:
            print("Set IP to {} for AAAA record '{}' for {}".format(ip, GANDI_RECORD, GANDI_DOMAIN))
    else:
        print("No change in external IP ({}), not updating AAAA record".format(ip))


if __name__ == '__main__':
    GANDI_URL = _get_env_var('GANDI_URL', 'https://dns.api.gandi.net/api/v5/')
    GANDI_KEY = _get_env_var('GANDI_KEY', False)
    GANDI_DOMAIN = _get_env_var('GANDI_DOMAIN', False)
    GANDI_RECORD = _get_env_var('GANDI_RECORD', '@')
    update_a_record()
    update_aaaa_record()
