# ── Stage 1 : récupération du binaire Shoutrrr ──────────────────────────────
FROM alpine:3.21 AS shoutrrr-fetcher

ARG SHOUTRRR_VERSION=0.8.0

RUN apk add --no-cache curl \
 && curl -fsSL \
    "https://github.com/containrrr/shoutrrr/releases/download/v${SHOUTRRR_VERSION}/shoutrrr_linux_amd64" \
    -o /usr/local/bin/shoutrrr \
 && chmod +x /usr/local/bin/shoutrrr

# ── Stage 2 : image finale ───────────────────────────────────────────────────
FROM python:3.14-alpine

LABEL org.opencontainers.image.title="Gandi DDNS"
LABEL org.opencontainers.image.description="Dynamic DNS Update Client for Gandi's LiveDNS"
LABEL org.opencontainers.image.authors="Winston Astrachan"
LABEL org.opencontainers.image.source="https://github.com/wastrachan/docker-gandi-ddns/"
LABEL org.opencontainers.image.licenses="MIT"

COPY --from=shoutrrr-fetcher /usr/local/bin/shoutrrr /usr/local/bin/shoutrrr

COPY app/ /
RUN set -eux; \
    pip install -r /requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["crond", "-f", "-c", "/etc/crontabs/"]
