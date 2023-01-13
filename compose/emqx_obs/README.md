# Deploy EMQX with Observability layer

This deployment includes EMQX with Prometheus + Grafana observability stack.
Prometheus is used for data collection and Grafana for using monitoring
dashboards. This way users can observe data and create alerts/events for and
from their hummingbot environments using cloud-native tools.

Use the `launch.sh` to start the deployment using docker compose.

```
➜ ./launch.sh

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
```

The default credentials for EMQX dashboard (http://localhost:18083) are: `admin/public`

The default credentials for Grafana dashboard (http://localhost:3000) are: `admin/admin`

**This is a demo deployment schema for local usage!! Do not use in
production!!**
