Docker Image Template
=====================

Software in a Docker container, with configuration files in a volume, and a configurable UID/GID for said files.

[![](https://circleci.com/gh/wastrachan/docker-image-template.svg?style=svg)](https://circleci.com/gh/wastrachan/docker-image-template)
[![](https://images.microbadger.com/badges/image/wastrachan/docker-image-template.svg)](https://microbadger.com/images/wastrachan/docker-image-template)
[![](https://img.shields.io/docker-image-template/pulls/wastrachan/docker-image-template.svg)](https://hub.docker-image-template.com/r/wastrachan/docker-image-template)

## Install

#### Docker Hub
Pull the latest image from Docker Hub:

```shell
docker pull wastrachan/docker-image-template
```

#### Manually
Clone this repository, and run `make build` to build an image:

```shell
git clone https://github.com/wastrachan/docker-image-template.git
cd docker-image-template
make build
```

If you need to rebuild the image, run `make clean build`.


## Run

#### Docker
Run this image with the `make run` shortcut, or manually with `docker run`.


```shell
docker run -v "$(pwd)/config:/config" \
           --name image-template \
           -e PUID=1111 \
           -e PGID=1112 \
           --restart unless-stopped \
           wastrachan/docker-image-template:latest
```


#### Docker Compose
If you wish to run this image with docker-compose, an example `docker-compose.yml` might read as follows:

```yaml
---
version: "2"

services:
  docker-image-template:
    image: wastrachan/docker-image-template
    container_name: docker-image-template
    environment:
      - PUID=1111
      - PGID=1112
    volumes:
      - </path/to/config>:/config
    ports:
      - 80:80/tcp
    restart: unless-stopped
```


## Configuration
Configuration files are stored in the `/config` volume. You may wish to mount this volume as a local directory, as shown in the examples above.


#### User / Group Identifiers
If you'd like to override the UID and GID of the application, you can do so with the environment variables `PUID` and `PGID`. This is helpful if other containers must access your configuration volume.

#### Services
Service     | Port
------------|-----
HTTP        | 80

#### Volumes
Volume          | Description
----------------|-------------
`/config`       | Configuration directory


## License
The content of this project itself is licensed under the [MIT License](LICENSE).

View license information for the software contained in this image.
