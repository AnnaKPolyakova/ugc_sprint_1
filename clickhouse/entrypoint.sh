#!/bin/bash

echo "start table creation"
docker exec -i node1 clickhouse-client -n <<-EOSQL
    DROP DATABASE IF EXISTS default;
    CREATE DATABASE IF NOT EXISTS default;
    CREATE TABLE IF NOT EXISTS default.movies_logs (event_time
    DateTime, user_id
    UUID, movie_id UUID, timestamp UInt32) ENGINE = Distributed('company_cluster', '', movies_logs, rand());
    CREATE DATABASE IF NOT EXISTS shard;
    CREATE TABLE IF NOT EXISTS shard.movies_logs (
    event_time DateTime,
    user_id UUID,
    movie_id UUID,
    timestamp UInt32
    ) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard1/movies_logs', 'replica_1')
    PARTITION BY toYYYYMMDD(event_time) ORDER BY event_time;
EOSQL

docker exec -i node2 clickhouse-client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS default;
    CREATE DATABASE IF NOT EXISTS replica;
    CREATE TABLE IF NOT EXISTS replica.movies_logs (event_time
    DateTime,
    user_id
    UUID, movie_id UUID, timestamp UInt32) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard1/movies_logs', 'replica_2')
    PARTITION BY toYYYYMMDD(event_time) ORDER BY event_time;
EOSQL

docker exec -i node3 clickhouse-client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS default;
    CREATE DATABASE IF NOT EXISTS shard;
    CREATE TABLE IF NOT EXISTS shard.movies_logs (event_time
    DateTime,
    user_id
    UUID, movie_id UUID, timestamp UInt32) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard2/movies_logs', 'replica_1')
    PARTITION BY toYYYYMMDD(event_time) ORDER BY event_time;
EOSQL

docker exec -i node4 clickhouse-client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS default;
    CREATE DATABASE IF NOT EXISTS replica;
    CREATE TABLE IF NOT EXISTS replica.movies_logs (event_time
    DateTime,
    user_id
    UUID, movie_id UUID, timestamp UInt32) Engine=ReplicatedMergeTree
    ('/clickhouse/tables/shard2/movies_logs', 'replica_2')
    PARTITION BY toYYYYMMDD(event_time) ORDER BY event_time;
EOSQL

echo "done"
