import logging
from datetime import datetime
from logging.config import dictConfig


logging_config = {
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
    }


dictConfig(logging_config)


def measure_time(func):
    def _wrapper(*args, **kwargs):
        try:
            start = datetime.now()
            func(*args, **kwargs)
        except Exception as error:
            logging.error(
                "Test ({test}) error: {error}".format(
                    test=func.__name__,
                    error=error
                )
            )
        else:
            logging.info(
                "Function: {func}, running time: {time}".format(
                    func=func.__name__,
                    time=datetime.now() - start
                )
            )
    return _wrapper
