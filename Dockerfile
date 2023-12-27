FROM amancevice/superset:1.5.1

USER root
RUN pip install clickhouse-connect
