#!/bin/sh

docker-compose up -d --build &&

docker images | grep none | awk '{print $3}' | xargs docker rmi
