import logging
import random
import uuid
from datetime import datetime
from time import sleep

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

from db_tests.cassandra.run_tests import OBJECT_COUNTS


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


class CassandraLoad:

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
        self.session.execute(
            "CREATE TABLE IF NOT EXISTS views (id text, user_id text, "
            "movie_id text, timestamp bigint, PRIMARY KEY(id));"
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

    def _insert(self):
        n = 0
        while True:
            sleep(0.01)
            try:
                objs = self._get_obj_list()
                self.session.execute(objs)
                n += 1
                logging.info(n)
            except Exception:
                pass

    def run(self):
        self._init_test_db()
        self._insert()


if __name__ == "__main__":
    load = CassandraLoad()
    load.run()
