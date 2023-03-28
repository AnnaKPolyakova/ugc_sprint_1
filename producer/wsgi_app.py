from gevent import monkey

monkey.patch_all()

from producer.producer_app import create_producer_app

app = create_producer_app()
