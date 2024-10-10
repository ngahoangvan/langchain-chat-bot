import os
from enum import Enum
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


# System
class Environment(str, Enum):
    TESTING = "TESTING"
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

    @property
    def is_deployed(self) -> bool:
        return self in (self.DEVELOPMENT, self.PRODUCTION)


class Config(BaseSettings):
    # Database
    DATABASE_URI: Optional[PostgresDsn] = os.getenv("DATABASE_URI", "")

    # Web Application
    CORS_ORIGINS: Optional[str] = ""
    CORS_ORIGINS_REGEX: Optional[str] = None
    CORS_HEADERS: Optional[str] = ""
    ENVIRONMENT: Optional[str] = Environment(Environment.LOCAL)
    SITE_DOMAIN: str = "localhost"

    # JWT
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = ""
    SECURE_COOKIES: bool = False

    # OpenAI
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    VERBOSE: bool = False

    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379")

    # Langfuse
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = ""

    # Slack
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_APP_TOKEN: str = os.getenv("SLACK_APP_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")

    # Vector Store
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    QDRANT_PORT: int = os.getenv("QDRANT_PORT", 443)
    QDRANT_GRPC_PORT: int = os.getenv("QDRANT_GRPC_PORT", 6334)

    # Elasticsearch loggin
    ELK_HOST: str = os.getenv("ELK_HOST", "localhost")
    ELK_PORT: int = os.getenv("ELK_PORT", 9200)
    ELK_INDEX: str = os.getenv("ELK_INDEX", "langchain-bot-logs")
    ELK_USERNAME: str = os.getenv("ELK_USERNAME", "")
    ELK_PASSWORD: str = os.getenv("ELK_PASSWORD", "")

    class Config:
        env_file = "./.env"
        extra = "allow"


settings = Config()
templates = Jinja2Templates(directory="templates")
app_configs: dict[str, Any] = {"title": "Chatbot API"}
