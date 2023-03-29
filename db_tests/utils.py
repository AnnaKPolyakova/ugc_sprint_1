import logging
from logging.config import dictConfig
from datetime import datetime, timedelta

TESTS_COUNT = 100

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
            max_value = timedelta(minutes=0)
            min_value = timedelta(minutes=0)
            all_result = []
            for _ in range(TESTS_COUNT):
                start = datetime.now()
                func(*args, **kwargs)
                result = datetime.now() - start
                all_result.append(result)
                if min_value > result or min_value == timedelta(minutes=0):
                    min_value = result
                if max_value < result or max_value == timedelta(minutes=0):
                    max_value = result
        except Exception as error:
            logging.error(
                "Test ({test}) error: {error}".format(
                    test=func.__name__,
                    error=error
                )
            )
        else:
            all_result.sort()
            all_result_len = len(all_result)
            if len(all_result) % 2 == 0:
                v1 = int(all_result_len/2 - 1)
                v2 = int(all_result_len/2)
                median = (all_result[v1] + all_result[v2]) / 2
            else:
                median = all_result[all_result_len // 2]
            logging.info(
                "Test: {func}, result: {min} - {max}, median: {median}".format(
                    func=func.__name__,
                    min=min_value,
                    max=max_value,
                    median=median
                )
            )
    return _wrapper
