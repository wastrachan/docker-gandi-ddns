# Gandi Dynamic DNS

Dynamic DNS Update Client for Gandi's LiveDNS.

[![](https://circleci.com/gh/wastrachan/docker-gandi-ddns.svg?style=svg)](https://circleci.com/gh/wastrachan/docker-gandi-ddns)
[![](https://img.shields.io/docker/pulls/wastrachan/gandi-ddns.svg)](https://hub.docker.com/r/wastrachan/gandi-ddns)

## Install

#### Docker Hub

Pull the latest image from Docker Hub:

```shell
docker pull wastrachan/gandi-ddns
```

#### Github Container Registry

Or, pull from the GitHub Container Registry:

```shell
docker pull ghcr.io/wastrachan/gandi-ddns
```

#### Build From Source

Clone this repository, and run `make build` to build an image:

```shell
git clone https://github.com/wastrachan/docker-gandi-ddns.git
cd gandi-ddns
make build
```

## Run

#### Docker

Run this image with the `make run` shortcut, or manually with `docker run`. You'll need to define several environment variables for this container, and they are detailed below.

```shell
docker run --name gandi-ddns \
           --rm \
           -e GANDI_PAT="12343123abcd" \
           -e GANDI_DOMAIN="mydomain.net" \
           wastrachan/gandi-ddns:latest
```

## Configuration

Configuration is accomplished through the use of environment variables. The inclusive list is below.

#### Environment Variables

| Variable          | Default                     | Description                                                                                                                                     |
| ----------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `GANDI_URL`       | `https://api.gandi.net/v5/` | URL of the Gandi API.                                                                                                                           |
| `GANDI_KEY`       | -                           | _DEPRECATED_ API Key for your [Gandi.net account](https://docs.gandi.net/en/domain_names/advanced_users/api.html)                               |
| `GANDI_PAT`       | -                           | Personal Access Token for your [Gandi.net account](https://docs.gandi.net/en/managing_an_organization/organizations/personal_access_token.html) |
| `GANDI_DOMAIN`    | -                           | Your Gandi.net domain name                                                                                                                      |
| `GANDI_RECORD`    | `@`                         | Record to update with your IP address                                                                                                           |
| `GANDI_TTL`       | -                           | TTL in seconds for the updated records                                                                                                          |
| `UPDATE_SCHEDULE` | `*/5 * * * *`               | Cron-style schedule for dynamic-dns updates.                                                                                                    |
| `SHOUTRRR_URL`    | -                           | Optional [Shoutrrr](https://containrrr.dev/shoutrrr/services/overview) notification URL. If set, a notification is sent on every DNS update.   |

## Notifications

This image supports push notifications via [Shoutrrr](https://containrrr.dev/shoutrrr) when a DNS record is updated. Set the `SHOUTRRR_URL` environment variable with the URL of your desired provider:

```shell
# ntfy
docker run --name gandi-ddns \
           --rm \
           -e GANDI_PAT="12343123abcd" \
           -e GANDI_DOMAIN="mydomain.net" \
           -e SHOUTRRR_URL="ntfy://ntfy.sh/my-topic" \
           wastrachan/gandi-ddns:latest

# Telegram
docker run --name gandi-ddns \
           --rm \
           -e GANDI_PAT="12343123abcd" \
           -e GANDI_DOMAIN="mydomain.net" \
           -e SHOUTRRR_URL="telegram://BOT_TOKEN@telegram?chats=CHAT_ID" \
           wastrachan/gandi-ddns:latest

# Discord
docker run --name gandi-ddns \
           --rm \
           -e GANDI_PAT="12343123abcd" \
           -e GANDI_DOMAIN="mydomain.net" \
           -e SHOUTRRR_URL="discord://TOKEN@WEBHOOK_ID" \
           wastrachan/gandi-ddns:latest
```

For the full list of supported providers and URL formats, see the [Shoutrrr documentation](https://containrrr.dev/shoutrrr/services/overview).

## License

The content of this project itself is licensed under the [MIT License](LICENSE).
