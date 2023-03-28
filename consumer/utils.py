import logging
import uuid

from spectree import SpecTree
from kafka import KafkaConsumer
from datetime import datetime, timedelta

from clickhouse_driver import Client

from consumer.settings import KAFKA_URL, consumer_settings

consumer_doc = SpecTree(
    "flask", title='Consumer API documentation', version='v1', path='v1/doc/'
)


class ConsumerManager:
    def __init__(self):
        self.client = Client(host=consumer_settings.CLICKHOUSE_HOST)

    def put_data_to_db(self):
        logging.info("kafka url: {url}".format(url=KAFKA_URL))
        try:
            consumer = KafkaConsumer(
                consumer_settings.TOPIC,
                bootstrap_servers=[KAFKA_URL],
                auto_offset_reset='earliest',
                group_id=consumer_settings.GROUP_ID,
            )
        except Exception as error:
            logging.error("consumer error: {error}".format(error=error))
        else:
            logging.info("consumer: {consumer}".format(consumer=consumer))
            for message in consumer:
                try:
                    logging.info("Start save message to db")
                    self.client.execute(
                        "INSERT INTO default.movies_logs ("
                        "event_time, user_id, movie_id, timestamp"
                        ") VALUES", [
                            (
                                datetime.utcnow(),
                                uuid.UUID(message.key.decode('utf-8')[:36]),
                                uuid.UUID(message.key.decode('utf-8')[36:]),
                                int(message.value.decode('utf-8')),
                            )
                        ]
                    )
                except Exception as error:
                    logging.error(
                        "Can not save message to db, error: {error}".format(
                            error=error
                        )
                    )
                else:
                    logging.info(
                        "Message was saved in db: {key}".format(key=message.key)
                    )
