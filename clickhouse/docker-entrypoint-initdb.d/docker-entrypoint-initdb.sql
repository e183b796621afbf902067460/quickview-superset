-- Actual database to store the data
CREATE DATABASE IF NOT EXISTS clickhouse;

-- Actual table to store the data fetched from an Apache Kafka topic
CREATE TABLE IF NOT EXISTS clickhouse.dm_real_time_tx_processing
(
    dm_real_time_tx_processing_address           String,

    dm_real_time_tx_processing_swap_maker        String,
    dm_real_time_tx_processing_tx_hash           String,

    dm_real_time_tx_processing_t0_symbol         String,
    dm_real_time_tx_processing_t1_symbol         String,
    dm_real_time_tx_processing_t0_amount         Float64,
    dm_real_time_tx_processing_t1_amount         Float64,

    dm_real_time_tx_processing_protocol          String,
    dm_real_time_tx_processing_blockchain        String,

    dm_real_time_tx_processing_swap_side         String    DEFAULT if(dm_real_time_tx_processing_t0_amount > 0, 'SELL', 'BUY'),
    dm_real_time_tx_processing_swap_quote_price  Float64   DEFAULT abs(dm_real_time_tx_processing_t1_amount / dm_real_time_tx_processing_t0_amount),

    dm_real_time_tx_processing_timestamp         DateTime
)
ENGINE = MergeTree
PARTITION BY toYYYYMMDD(dm_real_time_tx_processing_timestamp)
ORDER BY dm_real_time_tx_processing_timestamp;

-- Kafka Engine which consumes the data from 'app.topic' of Apache Kafka
CREATE TABLE IF NOT EXISTS clickhouse.q_real_time_tx_processing
(
    q_real_time_tx_processing_address           String,

    q_real_time_tx_processing_swap_maker        String,
    q_real_time_tx_processing_t0_symbol         String,
    q_real_time_tx_processing_t1_symbol         String,
    q_real_time_tx_processing_t0_amount         Float64,
    q_real_time_tx_processing_t1_amount         Float64,

    q_real_time_tx_processing_tx_hash           String,

    q_real_time_tx_processing_protocol          String,
    q_real_time_tx_processing_blockchain        String,

    q_real_time_tx_processing_timestamp         DateTime
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'topic',
    kafka_group_name = 'q_real_time_tx_processing_ch',
    kafka_format = 'JSONEachRow';

-- Materialized View to insert any consumed data by Kafka Engine to 'dm_real_time_tx_processing' table
CREATE MATERIALIZED VIEW IF NOT EXISTS clickhouse.mv_real_time_tx_processing TO clickhouse.dm_real_time_tx_processing AS
SELECT
    q_real_time_tx_processing_address AS dm_real_time_tx_processing_address,
    q_real_time_tx_processing_swap_maker AS dm_real_time_tx_processing_swap_maker,
    q_real_time_tx_processing_t0_symbol AS dm_real_time_tx_processing_t0_symbol,
    q_real_time_tx_processing_t1_symbol AS dm_real_time_tx_processing_t1_symbol,
    q_real_time_tx_processing_t0_amount AS dm_real_time_tx_processing_t0_amount,
    q_real_time_tx_processing_t1_amount AS dm_real_time_tx_processing_t1_amount,
    q_real_time_tx_processing_tx_hash AS dm_real_time_tx_processing_tx_hash,
    q_real_time_tx_processing_protocol AS dm_real_time_tx_processing_protocol,
    q_real_time_tx_processing_blockchain AS dm_real_time_tx_processing_blockchain,
    q_real_time_tx_processing_timestamp AS dm_real_time_tx_processing_timestamp
FROM
    clickhouse.q_real_time_tx_processing;