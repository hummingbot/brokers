#!/usr/bin/env bash

docker-compose -f emqx.compose.yml down --remove-orphans &&
    # docker compose -f emqx.compose.yml run emqx1
    docker compose -f emqx.compose.yml up --remove-orphans
