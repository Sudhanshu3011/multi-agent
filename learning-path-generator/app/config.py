import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    TAVILY_API_KEY: str = ""
    SERPAPI_API_KEY: str = ""
    GITHUB_TOKEN: str = ""
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE: float = 0.3
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Directory settings
    APP_DIR: str = os.path.dirname(os.path.abspath(__file__))
    PROMPTS_DIR: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "prompts"
    )


settings = Settings()
