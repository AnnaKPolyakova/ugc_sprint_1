from pydantic import BaseModel


class LogsCreate(BaseModel):
    movie_id: str
    user_id: str
    timestamp: int
