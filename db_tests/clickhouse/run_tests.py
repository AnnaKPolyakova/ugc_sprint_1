import logging
import random
import uuid
from datetime import datetime

from clickhouse_driver import Client

from db_tests.utils import measure_time

OBJECT_COUNTS = 100


def get_obj_list(number=OBJECT_COUNTS):
    objs = []
    for _ in range(0, number):
        objs.append(
            (
                datetime.utcnow(),
                uuid.uuid4(),
                uuid.uuid4(),
                random.randint(0, 100),
            )
        )
    return objs


class ClickhouseTest:
    def __init__(self):
        self.client = Client(host='localhost')

    def _init_test_db(self):
        self.client.execute(
            "DROP DATABASE IF EXISTS test ON CLUSTER company_cluster"
        )
        self.client.execute(
            "CREATE DATABASE IF NOT EXISTS test ON CLUSTER company_cluster"
        )
        self.client.execute("""
             CREATE TABLE IF NOT EXISTS test.views ON CLUSTER company_cluster
             (event_time DateTime, user_id UUID,
             movie_id UUID, timestamp UInt32)
             Engine=MergeTree() ORDER BY event_time
         """)

    @measure_time
    def _insert_test(self):
        logging.info("Start insert_test")
        objs = get_obj_list()
        self.client.execute(
            "INSERT INTO test.views ("
            "event_time, user_id, movie_id, timestamp"
            ") VALUES", objs
        )
        logging.info("End test insert_test")

    @measure_time
    def _get_test(self):
        logging.info("Start get_test")
        self.client.execute("SELECT * FROM test.views")
        logging.info("End test get_test")

    def run_tests(self):
        self._init_test_db()
        self._insert_test()
        self._get_test()


if __name__ == "__main__":
    tests = ClickhouseTest()
    tests.run_tests()
