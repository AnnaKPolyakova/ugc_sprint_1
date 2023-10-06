# Sprint 8 project work

API for loading analytical data into kafka -> clickhouse

Technologies and requirements:
```
Python 3.9+
kafka
clickhouse
```

### Docker Settings

##### Installation

* [Detailed installation guide](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Docker-compose settings

##### Installation

* [Detailed Installation Guide](https://docs.docker.com/compose/install/)

### Launch the application

#### Before starting the project, create environment variables
Create a .env in the root and add the necessary variables to it
Example in .env.example - to run the entire application in docker
Example in .env.example-local - to run the application locally and partially in docker

#### Run completely in docker containers:
kafka, api (producer), consumer (saves data), clickhouse

* `docker-compose -f docker-compose-api.yml up -d --build`
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml up -d --build`
* `chmod +x clickhouse/entrypoint.sh` - make the file executable
* `clickhouse/entrypoint.sh` - start creating tables on shards

To stop the container:
* `docker-compose -f docker-compose-api.yml down --rmi all --volumes`
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml down --rmi all --volumes`


#### Running the project partially in docker containers (kafka, clickhouse)

* `docker-compose -f docker-compose-api-local.yml up -d --build`
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml up -d --build`
* `python -m consumer.consumer_app`
* `python -m producer.producer_app`
* `chmod +x clickhouse/entrypoint.sh` - make the file executable
* `clickhouse/entrypoint.sh` - start creating tables on shards

To stop the container:
* `docker-compose -f docker-compose-api-local.yml down --rmi all --volumes`
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml down --rmi all --volumes`


Documentation at:
http://127.0.0.1:8003/v1/doc/redoc/ or or
http://127.0.0.1:8003/v1/doc/swagger/


### Testing

The results will be displayed in the terminal

#### Testing clickhouse
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml up -d --build`
* `python -m db_tests.clickhouse.run_tests`

If necessary, start loading data for the load in parallel:
* `python -m db_tests.clickhouse.run_load.py`

#### Testing cassandra
* `docker-compose -f db_tests/cassandra/docker-compose_cassandra.yml up -d --build`
* `python -m db_tests.cassandra.run_tests`

If necessary, start loading data for the load in parallel:
* `python -m db_tests.cassandra.run_load.py`


[Research results](db_tests%2Fresearch_results.md)
