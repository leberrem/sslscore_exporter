# sslscore-exporter

Docker image to export metrics from sslscore API to prometheus

**Parameters**

- port : http port (default : 9299)
- interval : interval between collect in seconds (default: 60)
- HOST : host key

**docker compose sample**

```yml
version: "2.1"

services:

  ssllabs_exporter:
    image: registre.mgcloud.fr/mgdis/ssllabs-exporter:1.0
    container_name: ssllabs_exporter
    ports:
      - "9299:9299"
    environment:
      - HOST=github.com
```
