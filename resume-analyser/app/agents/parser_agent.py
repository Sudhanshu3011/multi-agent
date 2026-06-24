from app.agents.base_agent import BaseAgent
from app.core.logger import get_logger
from app.graph.state import ResumeState

logger = get_logger(__name__)


class ParserAgent(BaseAgent):
    """
    Node 1: Asks the LLM to segment the extracted resume text into structured sections (experience, education, skills, etc.).
    """

    prompt_file = "parser_agent.yaml"

    def __init__(self) -> None:
        super().__init__()
        self._prompt = self._load_prompt()

    def run(self, state: ResumeState) -> dict:
        logger.info("ParserAgent started")

        if state.get("error"):
            logger.warning("Skipping — upstream error detected")
            return {}

        raw_text = state.get("extracted_text", "")
        if not raw_text:
            logger.error("No extracted_text found in state")
            return {"error": "No extracted text found in state."}

        # LLM: segment into sections
        try:
            messages = self._build_messages(
                resume_text=raw_text[:6000]
            )  # stay under token limit
            response = self.llm.invoke(messages)
            parsed = self._parse_json_response(response.content)
            logger.info(
                f"Parsed sections for: {parsed.get('candidate_name', 'Unknown')}"
            )
            return {
                "parsed_sections": parsed,
            }
        except Exception as exc:
            logger.exception("Section parsing failed")
            raise exc
