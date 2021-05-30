#!/bin/bash

docker system prune -f -a
pipenv update --dev
pipenv lock --dev -r > requirements.txt
docker compose up --build
