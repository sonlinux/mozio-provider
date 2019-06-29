#!/usr/bin/env bash
IMAGE_NAME=mozio_nginx
TAG_NAME=latest
docker build --no-cache -t mukomalison/${IMAGE_NAME} .
docker tag mukomalison/${IMAGE_NAME}:latest mukomalison/${IMAGE_NAME}:${TAG_NAME}
docker push mukomalison/${IMAGE_NAME}:${TAG_NAME}
