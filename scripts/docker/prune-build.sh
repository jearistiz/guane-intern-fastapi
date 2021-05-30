#!/bin/bash

docker system prune -a
pipenv update --dev
pipenv lock --dev -r > requirements.txt
docker compose up --build
