# quickview-superset

[![license](https://img.shields.io/:license-Apache%202-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0.txt)

# Docker

- Start all services to deploy needed environment:

```bash
docker-compose up -d --build --force-recreate
```

- Stop all services:

```bash
docker-compose down -v
```

That's important to remove all the volumes because it could cause any error in the future setups.
> dogacan. (2021). [Apache Superset error when installing locally using Docker Compose](https://stackoverflow.com/questions/68060234/apache-superset-error-when-installing-locally-using-docker-compose).

# Versions

- The `latest` tag points to the latest release of the latest stable branch.

# Volumes

- `/etc/superset/` — folder with superset configuration.
- `/app/docker-entrypoint-initdb.d/` — scripts to run on Apache Superset container start.
- `/app/docker-entrypoint-superset-on-startup.sh` — script to run Apache Superset with pre-configured assets.

# Configuration

### Node environment variables

- `WSS_NODE_PROVIDER`: WebSocket node provider. 

### Superset environment variables

- `SECRET_KEY`: Superset application secret key.
