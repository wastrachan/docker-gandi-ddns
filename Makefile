# Gandi DDNS Docker Image

.PHONY: help
help:
	@echo ""
	@echo "Usage: make COMMAND"
	@echo ""
	@echo "Docker gandi-ddns image makefile"
	@echo ""
	@echo "Commands:"
	@echo "  build        Build and tag image"
	@echo "  push         Push tagged image to registry"
	@echo "  run          Start container in the background with locally mounted volume"
	@echo "  stop         Stop and remove container running in the background"
	@echo "  delete       Delete all built image versions"
	@echo ""

IMAGE=wastrachan/gandi-ddns
TAG=latest
REGISTRY=docker.io

.PHONY: build
build:
	@docker build -t ${REGISTRY}/${IMAGE}:${TAG} .

.PHONY: push
push:
	@docker push ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: run
run: build
	docker run --name gandi-ddns \
			   --rm \
	           -e GANDI_KEY="12343123abcd" \
			   -e GANDI_DOMAIN="mydomain.net" \
	           -d \
	           ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: stop
stop:
	@docker stop gandi-ddns

.PHONY: delete
delete:
	@docker image ls | grep ${IMAGE} | awk '{print $$3}' | xargs -I + docker rmi +
