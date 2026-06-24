from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

    serpapi_api_key: str

    log_level: str = "INFO"

    langsmith_api_key: str | None = None
    langsmith_project: str = "resume-analyser"
    langsmith_tracing: bool = True
    langsmith_endpoint: str = "https://api.smith.langchain.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
