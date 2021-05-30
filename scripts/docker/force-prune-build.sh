#!/bin/bash

docker system prune -f -a
docker compose up --build
