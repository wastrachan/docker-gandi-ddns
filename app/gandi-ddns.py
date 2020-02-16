"""
Gandi Dynamic DNS

Dynamic DNS Update Client for Gandi's LiveDNS

Copyright (C) 2020 Winston Astrachan
Released under the terms of the MIT license
"""
import os
import requests


def get_env_var(name, default=None):
    """ Return environment variable for 'name'

    If environment variable is not set:
        Return "default"

    If "default" is False:
        Raise ValueError
    """
    try:
        return os.environ[name]
    except KeyError:
        if default is False:
            raise ValueError("The {} environment variable is required but not set.".format(name))
        return default


GANDI_URL = get_env_var('GANDI_URL', 'https://dns.api.gandi.net/api/v5/')
GANDI_KEY = get_env_var('GANDI_KEY', False)
GANDI_DOMAIN = get_env_var('GANDI_DOMAIN', False)
GANDI_RECORD = get_env_var('GANDI_RECORD', '@')


def get_ipv4():
    """ Returns current, public IPV4 address """
    response = requests.get('https://ipv4.icanhazip.com/')
    return response.text.strip()


def get_ipv6():
    """ Returns current, public IPV6 address """
    response = requests.get('https://ipv6.icanhazip.com/')
    return response.text.strip()


def get_headers():
    """ Returns API request headers for the Gandi API """
    return {
        'X-Api-Key': GANDI_KEY,
        'Content-Type': 'application/json',
    }


def update_a_record():
    """ Update A Records """
    try:
        ip = get_ipv4()
    except Exception as e:
        print("Unable to fetch current IPV4 address: {}".format(e))
    else:
        try:
            payload = {'rrset_values': ['{}'.format(ip)]}
            response = requests.put("{}domains/{}/records/{}/A".format(GANDI_URL, GANDI_DOMAIN, GANDI_RECORD),
                                    json=payload,
                                    headers=get_headers())
            response.raise_for_status()
        except Exception as e:
            print("Unable to update DNS record: {}".format(e))
        else:
            print("Updated record. Set IP to {} for A record {} for {}".format(ip, GANDI_RECORD, GANDI_DOMAIN))


def update_aaaa_record():
    """ Update AAAA Records """
    try:
        ip = get_ipv6()
    except Exception as e:
        print("Unable to fetch current IPV6 address: {}".format(e))
    else:
        try:
            payload = {'rrset_values': ['{}'.format(ip)]}
            response = requests.put("{}domains/{}/records/{}/AAAA".format(GANDI_URL, GANDI_DOMAIN, GANDI_RECORD),
                                    json=payload,
                                    headers=get_headers())
            print(response.text)
            response.raise_for_status()
        except Exception as e:
            print("Unable to update DNS record: {}".format(e))
        else:
            print("Updated record. Set IP to {} for AAAA record {} for {}".format(ip, GANDI_RECORD, GANDI_DOMAIN))


if __name__ == '__main__':
    update_a_record()
    update_aaaa_record()
