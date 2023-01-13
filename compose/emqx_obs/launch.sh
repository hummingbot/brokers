#!/usr/bin/env bash

echo -e """
Deployment includes:
[*] - EMQX single node
[*] - Prometheus
[*] - Grafana

Deploymeny exposes ports:
[*] - 1883  mqtt:tcp
[*] - 8883  mqtt:tcp:ssl / mqtts
[*] - 8083  mqtt:ws
[*] - 8084  mqtt:ws:ssl / mqtt:wss
[*] - 8081  http:emqx-management
[*] - 18083 http:emqx-dashboard
[*] - 3000  http:grafana
[*] - 9090  http:prometheus
"""
docker compose -f emqx.compose.yml down --remove-orphans &&
    # docker compose -f emqx.compose.yml run emqx1
    docker compose -f emqx.compose.yml up --remove-orphans
