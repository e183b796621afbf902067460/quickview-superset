# quickview-superset

[![license](https://img.shields.io/:license-Apache%202-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0.txt)

# Docker

- Start all services to deploy needed environment:

```bash
docker-compose up -d --build --force-recreate
```

- Stop all services:

```bash
docker-compose down
```

# Versions

- The `latest` tag points to the latest release of the latest stable branch.

# Volumes

- `/superset/` — folder with superset configuration.

# Configuration

### Superset environment variables

- `CACHE_REDIS_HOST`: Superset application Redis host.
- `CACHE_REDIS_PORT`: Superset application Redis port.
- `CACHE_REDIS_DB`: Superset application Redis database.
- `CACHE_REDIS_URL`: Superset application Redis URL.
- `SQLALCHEMY_DATABASE_URI`: Superset application PostgreSQL URI.
- `SECRET_KEY`: .Superset application secret key.
