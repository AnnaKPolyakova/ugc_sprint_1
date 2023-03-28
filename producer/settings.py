import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).resolve()

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class Settings(BaseSettings):
    KAFKA_HOST: str
    KAFKA_PORT: int
    TOPIC: str

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


producer_settings = Settings()
KAFKA_URL = "{host}:{port}".format(
    host=producer_settings.KAFKA_HOST,
    port=producer_settings.KAFKA_PORT
)