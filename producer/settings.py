import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).resolve()

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class Settings(BaseSettings):
    kafka_host: str
    kafka_port: int
    topic: str

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


producer_settings = Settings()
KAFKA_URL = "{host}:{port}".format(
    host=producer_settings.kafka_host,
    port=producer_settings.kafka_port
)
