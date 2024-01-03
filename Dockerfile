FROM apache/superset:1.5.1

USER root
RUN pip install clickhouse-connect

COPY ./etc/superset/superset_config.py /etc/superset/superset_config.py
COPY ./docker-entrypoint-initdb.d/ /app/docker-entrypoint-initdb.d/
COPY ./scripts/docker-entrypoint-superset-on-startup.sh /app/docker-entrypoint-superset-on-startup.sh

ENV SUPERSET_CONFIG_PATH /etc/superset/superset_config.py

CMD ["bash", "docker-entrypoint-superset-on-startup.sh"]
