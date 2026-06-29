.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help message
	@echo ""
	@echo "Docker gandi-ddns Makefile"
	@echo "Usage: make [target]"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} \
		/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5); next } \
		/^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' \
		$(MAKEFILE_LIST)
	@echo ""

IMAGE=wastrachan/gandi-ddns
TAG=latest
REGISTRY=docker.io

.PHONY: build
build:  ## Build and tag image
	@docker build -t ${REGISTRY}/${IMAGE}:${TAG} .

.PHONY: push
push:  ## Push tagged image to registry
	@docker push ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: run
run: build  ## Start container in the background with locally mounted volume
	docker run --name gandi-ddns \
			   --rm \
	           -e GANDI_PAT="12343123abcd" \
			   -e GANDI_DOMAIN="mydomain.net" \
	           -d \
	           ${REGISTRY}/${IMAGE}:${TAG}

.PHONY: stop
stop:  ## Stop and remove container running in the background
	@docker stop gandi-ddns

.PHONY: delete
delete:  ## Delete all built image versions
	@docker image ls | grep ${IMAGE} | awk '{print $$3}' | xargs -I + docker rmi +
