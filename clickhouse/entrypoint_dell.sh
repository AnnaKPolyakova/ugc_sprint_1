#!/bin/bash

echo "start table creation"
docker exec -i node1 clickhouse-client -n <<-EOSQL
    DROP DATABASE IF EXISTS default;
    CREATE DATABASE IF NOT EXISTS default;
    DROP DATABASE IF EXISTS logs_shard;
EOSQL

docker exec -i node2 clickhouse-client -n <<-EOSQL
    DROP DATABASE IF EXISTS logs_replica;
EOSQL

docker exec -i node3 clickhouse-client -n <<-EOSQL
    DROP DATABASE IF EXISTS logs_shard;
EOSQL

docker exec -i node4 clickhouse-client -n <<-EOSQL
    DROP DATABASE IF EXISTS logs_replica;
EOSQL

echo "done"
