# Use the official ClickHouse image as the base image
FROM clickhouse/clickhouse-server:23.1-alpine

ENV CLICKHOUSE_DB=clickhouse

ENV CLICKHOUSE_USER=clickhouse
ENV CLICKHOUSE_PASSWORD=clickhouse

COPY ./docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/
