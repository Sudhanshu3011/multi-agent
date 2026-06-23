import os
import logging
import yaml
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langchain_groq import ChatGroq
from app.config import settings

logger = logging.getLogger(__name__)


# ── typed exceptions ───────────────────────────────────────────────────────────


class AgentError(Exception):
    """Base exception for all agent errors."""


class LLMNotConfiguredError(AgentError):
    """LLM is required but GROQ_API_KEY is not set."""


class InvalidLLMResponseError(AgentError):
    """LLM returned a response that cannot be parsed into the expected structure."""


# ── base class ─────────────────────────────────────────────────────────────────


class BaseAgent(ABC):
    def __init__(self, prompt_file: str):
        self.prompt_file = prompt_file
        self.prompts = self._load_prompts()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _load_prompts(self) -> Dict[str, Any]:
        prompt_path = os.path.join(settings.PROMPTS_DIR, self.prompt_file)
        if not os.path.exists(prompt_path):
            logger.warning(
                "Prompt file not found: %s — using built-in defaults.", prompt_path
            )
            return {
                "system_prompt": "You are a helpful agent.",
                "user_prompt_template": "{input}",
            }
        with open(prompt_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_llm(self) -> ChatGroq:
        """Return the configured LLM or raise LLMNotConfiguredError."""
        if not settings.GROQ_API_KEY:
            raise LLMNotConfiguredError(
                f"{self.__class__.__name__} requires a Groq LLM. "
                "Set GROQ_API_KEY in your environment or .env file."
            )
        return ChatGroq(
            temperature=settings.LLM_TEMPERATURE,
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.LLM_MODEL,
        )

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        pass
