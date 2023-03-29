import logging
import random
import uuid
from datetime import datetime
from time import sleep

from clickhouse_driver import Client

from db_tests.clickhouse.run_tests import OBJECT_COUNTS


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


class ClickhouseLoad:
    def __init__(self):
        self.client = Client(host='localhost')

    def _init_test_db(self):
        self.client.execute(
            "CREATE DATABASE IF NOT EXISTS test ON CLUSTER company_cluster"
        )
        self.client.execute("""
             CREATE TABLE IF NOT EXISTS test.views ON CLUSTER company_cluster
             (event_time DateTime, user_id UUID,
             movie_id UUID, timestamp UInt32)
             Engine=MergeTree() ORDER BY event_time
         """)

    def _insert(self):
        n = 0
        while True:
            sleep(0.01)
            objs = get_obj_list()
            try:
                self.client.execute(
                    "INSERT INTO test.views ("
                    "event_time, user_id, movie_id, timestamp"
                    ") VALUES", objs
                )
                n += 1
                logging.info(n)
            except Exception:
                pass

    def run(self):
        self._init_test_db()
        self._insert()


if __name__ == "__main__":
    load = ClickhouseLoad()
    load.run()
