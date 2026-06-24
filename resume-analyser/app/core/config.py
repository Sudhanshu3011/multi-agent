import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    SERPAPI_API_KEY: str = ""

    GROQ_MODEL: str = "llama-3.1-8b-instant"

    LOG_LEVEL: str = "INFO"

    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "resume-analyser"
    LANGSMITH_TRACING: bool = True
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"

    APP_DIR: str = os.path.dirname(os.path.abspath(__file__))
    PROMPTS_DIR: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "prompts"
    )


settings = Settings()
