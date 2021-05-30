#!/bin/bash

pipenv --rm
pipenv update --dev
pipenv lock --dev -r > requirements.txt
pipenv run tests
