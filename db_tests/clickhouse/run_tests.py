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
        objs = get_obj_list()
        self.client.execute(
            "INSERT INTO test.views ("
            "event_time, user_id, movie_id, timestamp"
            ") VALUES", objs
        )

    @measure_time
    def _get_test(self):
        self.client.execute("SELECT * FROM test.views")

    def _get_test_from_full_db(self):
        self._init_test_db()
        for _ in range(50000):
            objs = get_obj_list(number=400)
            self.client.execute(
                "INSERT INTO test.views ("
                "event_time, user_id, movie_id, timestamp"
                ") VALUES", objs
            )

        @measure_time
        def start_get_test_from_full_db():
            self.client.execute("SELECT * FROM test.views")

        @measure_time
        def start_get_part_test_from_full_db():
            self.client.execute(
                "SELECT * FROM test.views WHERE timestamp = 1"
            )

        @measure_time
        def start_get_sum_test_from_full_db():
            self.client.execute(
                "SELECT sum(timestamp) FROM test.views WHERE timestamp > 50"
            )

        start_get_test_from_full_db()
        start_get_part_test_from_full_db()
        start_get_sum_test_from_full_db()

    def run_tests(self):
        self._init_test_db()
        self._insert_test()
        self._get_test()
        self._get_test_from_full_db()


if __name__ == "__main__":
    tests = ClickhouseTest()
    tests.run_tests()
