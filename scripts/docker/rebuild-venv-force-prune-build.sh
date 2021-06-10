#!/bin/bash

sh scripts/app/rebuild_venv.sh
sh scripts/docker/force-prune-build.sh
