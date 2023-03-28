import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).resolve()

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class Settings(BaseSettings):
    KAFKA_HOST: str
    KAFKA_PORT: str
    TOPIC: str
    GROUP_ID: str
    CLICKHOUSE_HOST: str

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


consumer_settings = Settings()
KAFKA_URL = "{host}:{port}".format(
    host=consumer_settings.KAFKA_HOST,
    port=consumer_settings.KAFKA_PORT
)
