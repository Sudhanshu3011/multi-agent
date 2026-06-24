from abc import ABC, abstractmethod
from pathlib import Path
import yaml
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


class BaseAgent(ABC):
    """
    Abstract base for all agents.
    Subclasses must implement `run(state)` and declare `prompt_file`.
    """

    prompt_file: str

    def __init__(self) -> None:
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0,
        )
        self._prompt = None

    def _load_prompt(self) -> dict:
        path = PROMPTS_DIR / self.prompt_file
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _build_messages(self, **kwargs) -> list:

        if self._prompt is None:
            self._prompt = self._load_prompt()

        system = self._prompt["system"].strip()
        user = self._prompt["user"].format(**kwargs).strip()

        return [
            SystemMessage(content=system),
            HumanMessage(content=user),
        ]

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
