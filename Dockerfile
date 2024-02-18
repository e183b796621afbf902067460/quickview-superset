FROM apache/superset:1.5.1

USER root
RUN pip install clickhouse-connect

COPY ./etc/superset/superset_config.py /etc/superset/superset_config.py

COPY ./docker-entrypoint-initdb.d/py /app/docker-entrypoint-initdb.d/
COPY ./docker-entrypoint-initdb.d/sh /app/docker-entrypoint-initdb.d/
COPY ./docker-entrypoint-initdb.d/zip /app/docker-entrypoint-initdb.d/

ENV SUPERSET_CONFIG_PATH /etc/superset/superset_config.py

CMD ["bash", "/app/docker-entrypoint-initdb.d/docker-entrypoint-initdb.sh"]
