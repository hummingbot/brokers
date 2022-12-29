# Deploy EMQX v4 broker using docker compose

To deploy [EMQX Broker](https://www.emqx.io/docs/en/v4.0/) run the `launch.sh` script

```
./launch.sh
```

The deployment exposes the following ports:

- 1883: `mqtt:tcp`
- 1884: `mqtt:tcp:ssl / mqtts:tcp`
- 1893: `mqtt:ws`
- 1894: `mqtt:ws:ssl / mqtt:wss`
- 8000: `http:management` - http://localhost:8000
- 8001: `http:dashboard` - http://localhost:8001

The default credentials for EMQX dashboard is `admin:public`.

Head to http://localhost:8001/ to configure EMQX broker.

**This is a demo deployment schema for local usage!! Do not use in
production!!**
