from gevent import monkey

monkey.patch_all()

from producer.producer_app import create_producer_app

from gevent.pywsgi import WSGIServer

app = create_producer_app()

if __name__ == "__main__":
    http_server = WSGIServer(("", 8003), app)
    http_server.serve_forever()
