import logging
from logging.config import dictConfig
from typing import List

from pydantic import AnyHttpUrl, BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "e-sports-semantic-search"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "test"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "ci_db"
    POSTGRES_PORT: int = 5432
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        env_file = "./.env"


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "lck-gamedata-logger"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


settings = Settings()
dictConfig(LogConfig().model_dump())
logger = logging.getLogger(settings.PROJECT_NAME)
