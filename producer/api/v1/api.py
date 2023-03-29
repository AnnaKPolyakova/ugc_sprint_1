import logging

from flask import Blueprint, request

from producer.api.v1.models.models import LogsCreate
from producer.utils import ProducerManager, producer_doc

producer_api = Blueprint("consumer", __name__)


@producer_api.route(
    '/', methods=["POST"]
)
@producer_doc.validate(
    tags=["consumer"],
    json=LogsCreate,
)
def producer():
    logging.debug("auth_proxy {name} start".format(name=producer.__name__))
    data = request.get_json()
    result, status = ProducerManager(
        data["movie_id"], data["user_id"], data["timestamp"]
    ).sent_message()
    return result, status
