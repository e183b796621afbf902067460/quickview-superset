FROM amancevice/superset:1.5.1

USER root
RUN pip install clickhouse-connect

COPY ./app/superset_config.py /etc/superset/superset_config.py
