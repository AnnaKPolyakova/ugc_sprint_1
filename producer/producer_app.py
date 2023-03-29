
from logging.config import dictConfig

from flask import Flask

from producer.api.v1.api import producer_api
from producer.utils import producer_doc


def create_producer_app():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })
    current_app = Flask(__name__)
    current_app.register_blueprint(producer_api, url_prefix="/producer")
    producer_doc.register(current_app)
    return current_app


if __name__ == "__main__":
    app = create_producer_app()
    app.run(port=8003)
