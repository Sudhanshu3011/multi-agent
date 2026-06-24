from abc import ABC, abstractmethod
from pathlib import Path
import yaml
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import get_settings
from app.core.logger import get_logger

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


class BaseAgent(ABC):
    """
    Abstract base for all agents.
    Subclasses must implement `run(state)` and declare `prompt_file`.
    """

    prompt_file: str

    def __init__(self) -> None:
        settings = get_settings()
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0,
        )
        self.logger = get_logger(self.__class__.__name__)
        self._prompt = self._load_prompt()

    def _load_prompt(self) -> dict:
        path = PROMPTS_DIR / self.prompt_file
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _build_messages(self, **kwargs) -> list:

        system = self._prompt["system"].strip()
        user = self._prompt["user"].format(**kwargs).strip()
        return [SystemMessage(content=system), HumanMessage(content=user)]

    def _parse_json_response(self, content: str) -> dict:
        """Strip markdown fences if present and parse JSON."""
        import json

        clean = content.strip()
        if clean.startswith("```"):
            lines = clean.splitlines()
            clean = (
                "\n".join(lines[1:-1])
                if lines[-1].strip() == "```"
                else "\n".join(lines[1:])
            )
        return json.loads(clean)

    @abstractmethod
    def run(self, state: dict) -> dict:
        """Execute agent logic and return a partial state update."""
        raise NotImplementedError
