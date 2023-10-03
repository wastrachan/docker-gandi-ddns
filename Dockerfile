FROM python:3.12-alpine
LABEL maintainer="Winston Astrachan"
LABEL description="Dynamic DNS Update Client for Gandi's LiveDNS"

COPY app/ /
RUN pip install -r /requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["crond", "-f", "-c", "/etc/crontabs/"]
