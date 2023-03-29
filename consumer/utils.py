import logging
import uuid
from datetime import datetime

from clickhouse_driver import Client
from kafka import KafkaConsumer, OffsetAndMetadata, TopicPartition
from spectree import SpecTree

from consumer.backoff import backoff
from consumer.settings import KAFKA_URL, consumer_settings

consumer_doc = SpecTree(
    "flask", title='Consumer API documentation', version='v1', path='v1/doc/'
)


class ConsumerManager:
    def __init__(self):
        self.client = Client(host=consumer_settings.clickhouse_host)

    @backoff()
    def put_data_to_db(self):
        logging.info("kafka url: {url}".format(url=KAFKA_URL))
        messages_batch = []
        try:
            consumer = KafkaConsumer(
                consumer_settings.topic,
                enable_auto_commit=False,
                bootstrap_servers=[KAFKA_URL],
                auto_offset_reset='earliest',
                group_id=consumer_settings.group_id,
            )
        except Exception as error:
            logging.error("consumer error: {error}".format(error=error))
        else:
            logging.info("consumer: {consumer}".format(consumer=consumer))
            for message in consumer:
                messages_batch.append(
                    (
                        datetime.utcnow(),
                        uuid.UUID(message.key.decode('utf-8')[:36]),
                        uuid.UUID(message.key.decode('utf-8')[36:]),
                        int(message.value.decode('utf-8'))
                    )
                )
                if len(messages_batch) < \
                        consumer_settings.clickhouse_batch_size:
                    continue
                try:
                    logging.info("Start save message to db")
                    self.client.execute(
                        "INSERT INTO default.movies_logs ("
                        "event_time, user_id, movie_id, timestamp"
                        ") VALUES", messages_batch
                    )
                except Exception as error:
                    logging.error(
                        "Can not save message to db, error: {error}".format(
                            error=error
                        )
                    )
                else:
                    offsets = {
                            TopicPartition(
                                consumer_settings.topic, 0
                            ): OffsetAndMetadata(message.offset + 1, None)
                        }
                    consumer.commit(offsets=offsets)
                    logging.info(
                        "Messages was saved in db: {mess}".format(
                            mess=messages_batch
                        )
                    )
                    messages_batch = []
