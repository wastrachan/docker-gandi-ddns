# Docker Image Makefile
#
# Copyright (c) Winston Astrachan 2019
#
help:
	@echo ""
	@echo "Usage: make COMMAND"
	@echo ""
	@echo "Docker Image makefile"
	@echo ""
	@echo "Commands:"
	@echo "  build        Build and tag image"
	@echo "  run          Start container in the background with locally mounted volume"
	@echo "  stop         Stop and remove container running in the background"
	@echo "  clean        Mark image for rebuild"
	@echo "  delete       Delete image and mark for rebuild"
	@echo ""

build: .docker-image-template.img

.docker-image-template.img:
	docker build -t wastrachan/docker-image-template:latest .
	@touch $@

.PHONY: run
run: build
	docker run -v "$(CURDIR)/config:/config" \
	           --name docker-image-template \
	           -e PUID=1111 \
	           -e PGID=1112 \
	           --restart unless-stopped \
	           -d \
	           wastrachan/docker-image-template:latest

.PHONY: stop
stop:
	docker stop docker-image-template
	docker rm docker-image-template

.PHONY: clean
clean:
	rm -f .docker-image-template.img

.PHONY: delete
delete: clean
	docker rmi -f wastrachan/docker-image-template
