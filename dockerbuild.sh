#!/bin/sh
docker buildx build --platform linux/amd64 -t $1:latest .
docker tag $1:latest cr.yandex/crp7qrc8eq1s7cvib51o/$1:latest
echo Login
docker push cr.yandex/crp7qrc8eq1s7cvib51o/$1:latest
