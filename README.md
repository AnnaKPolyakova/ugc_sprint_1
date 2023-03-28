# Проектная работа 8 спринта

Командная работа https://github.com/AnnaKPolyakova/ugc_sprint_1

API для загрузки аналитических данных в kafka -> clickhouse

Технологии и требования:
```
Python 3.9+
kafka
clickhouse
```

### Настройки Docker

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Настройки Docker-compose

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/compose/install/)

### Запуск приложения

#### Перед запуском проекта создаем переменные окружения
Создаем в корне .env и добавляем в него необходимые переменные  
Пример в .env.example - для запуска приложения целиком в docker  
Пример в .env.example-local - для запуска приложения локально и частично в docker

#### Запуск полностью в контейнерах docker: 
kafka, api (produсer), consumer (сохраняет данные), clickhouse

* `docker-compose -f docker-compose-api.yml up -d --build`
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml up -d --build`
* `chmod +x clickhouse/entrypoint.sh` - делаем файл исполняемым  
* `clickhouse/entrypoint.sh` - запускаем создание таблиц на шардах

Для остановки контейнера:  
* `docker-compose -f docker-compose-api.yml down --rmi all --volumes`
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml down --rmi all --volumes`


#### Запуск проекта частично в контейнерах docker (kafka, clickhouse)

* `docker-compose -f docker-compose-api-local.yml up -d --build`
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml up -d --build`
* `python -m consumer.consumer_app`
* `python -m producer.producer_app`
* `chmod +x clickhouse/entrypoint.sh` - делаем файл исполняемым  
* `clickhouse/entrypoint.sh` - запускаем создание таблиц на шардах

Для остановки контейнера:  
* `docker-compose -f docker-compose-api-local.yml down --rmi all --volumes`
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml down --rmi all --volumes`


Документация по адресу:
http://127.0.0.1:8003/v1/doc/redoc/ or или
http://127.0.0.1:8003/v1/doc/swagger/


### Тестирование  

Результаты будут отображены в терминале

#### Тестирование clickhouse
* `docker-compose -f clickhouse/docker-compose_clickhouse.yml up -d --build`
* `python -m db_tests.clickhouse.run_tests`

#### Тестирование cassandra
* `docker-compose -f db_tests/cassandra/docker-compose_cassandra.yml up -d --build`
* `python -m db_tests.cassandra.run_tests`
