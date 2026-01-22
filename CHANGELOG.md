# Changelog

## 1.4

- Add optional `GANDI_TTL` to set the TTL for the DNS record.
- Update dependencies
- Update base image to latest python3.14 alpine

## 1.3

- DEPRECATED: Switch from Gandi API tokens to Gandi PAT (personal access tokens). You should switch from `GANDI_KEY` TO `GANDI_PAT` as API tokens will be removed in a future version of this script
- Add type hints
- Update dependencies
- Update base image to latest python3.13 alpine

## 1.2

- Update dependencies
- Update base image to latest python3.12 alpine
- Format code with black

## 1.1.1

- Update requests to 2.28.0
- Update base image to latest python3.10 alpine

## 1.1

- Added caching for public addresses to avoid unneeded updates to the Gandi API.

## 1.0

- Initial release of Gandi Dynamic DNS.
