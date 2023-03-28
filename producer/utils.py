import logging
from datetime import timedelta
from http import HTTPStatus

from spectree import SpecTree
from kafka import KafkaProducer

from consumer.settings import KAFKA_URL, consumer_settings

producer_doc = SpecTree(
    "flask", title='Producer API documentation', version='v1', path='v1/doc/'
)


class ProducerManager:

    def __init__(self, movies_id: str, user_id: str, timestamp: timedelta):
        self.key: bytes = self._get_key(movies_id, user_id)
        self.movies_id = movies_id
        self.user_id = user_id
        self.value: bytes = bytes(str(timestamp), 'UTF-8')

    @staticmethod
    def _get_key(movies_id, user_id):
        return bytes(user_id + movies_id, 'UTF-8')

    def sent_message(self):
        try:
            logging.error(
                "Start {name}".format(name=self.sent_message.__name__)
            )
            producer = KafkaProducer(bootstrap_servers=[KAFKA_URL])
            producer.send(
                topic=consumer_settings.TOPIC,
                value=self.value,
                key=self.key,
                headers=[
                    ("user_id", bytes(self.user_id, 'UTF-8')),
                    ("movies_id", bytes(self.movies_id, 'UTF-8')),
                ]
            )
        except Exception as error:
            logging.error(
                "Get error {error} from {name}".format(
                    error=error,
                    name=self.sent_message.__name__
                )
            )
            return {"status": False}, HTTPStatus.BAD_REQUEST
        else:
            return {"status": True}, HTTPStatus.OK
