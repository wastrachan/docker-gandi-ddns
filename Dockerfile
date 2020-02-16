FROM alpine:latest
LABEL maintainer="Winston Astrachan"
LABEL description="Software on Alpine Linux"

RUN apk --no-cache add software
RUN mkdir /config

COPY overlay/ /
VOLUME /config
EXPOSE 80/tcp

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/sbin/software", "-c", "/config/named.conf"]
