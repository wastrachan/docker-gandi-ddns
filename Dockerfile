FROM python:3.12-alpine

LABEL org.opencontainers.image.title="Gandi DDNS"
LABEL org.opencontainers.image.description="Dynamic DNS Update Client for Gandi's LiveDNS"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Winston Astrachan"

COPY app/ /
RUN pip install -r /requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["crond", "-f", "-c", "/etc/crontabs/"]
