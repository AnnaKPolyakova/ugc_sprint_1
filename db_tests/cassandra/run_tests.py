import logging
import random
import uuid

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

from db_tests.utils import measure_time

OBJECT_COUNTS = 100


class CassandraTest:
    def __init__(self):
        self.session = self._get_session()

    @staticmethod
    def _get_session():
        cluster = Cluster(['127.0.0.1'], port=9042)
        session = cluster.connect()
        return session

    def _init_test_db(self):
        self.session.execute(
            "CREATE KEYSPACE IF NOT EXISTS test with replication = {"
            "'class' : 'SimpleStrategy', 'replication_factor':2"
            "}"
        )
        self.session.set_keyspace('test')
        self.session.execute(f"DROP TABLE IF EXISTS views;")
        self.session.execute(
            f"CREATE TABLE IF NOT EXISTS views (id text, user_id text, " \
            f"movie_id text, timestamp bigint, PRIMARY KEY(id));"
        )

    def _get_obj_list(self, number=OBJECT_COUNTS):
        insert_statement = self.session.prepare(
            """
            INSERT INTO views (id, user_id, movie_id, timestamp)
            VALUES (?, ?, ?, ?)
            """
        )
        batch = BatchStatement()
        for _ in range(0, number):
            batch.add(
                insert_statement,
                (
                    str(uuid.uuid4()),
                    str(uuid.uuid4()),
                    str(uuid.uuid4()),
                    random.randint(0, 100),
                )
            )
        return batch

    @measure_time
    def _insert_test(self):
        logging.info("Start insert_test")
        objs = self._get_obj_list()
        self.session.execute(objs)
        logging.info("End test insert_test")

    @measure_time
    def _get_test(self):
        logging.info("Start get_test")
        self.session.execute("SELECT * FROM views")
        logging.info("End test get_test")

    def run_tests(self):
        self._init_test_db()
        self._insert_test()
        self._get_test()


if __name__ == "__main__":
    tests = CassandraTest()
    tests.run_tests()
