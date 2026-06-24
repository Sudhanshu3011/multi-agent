from app.agents.base_agent import BaseAgent
from app.core.errors import ParserAgentError
from app.graph.state import ResumeState


class ParserAgent(BaseAgent):
    """
    Node 1: Asks the LLM to segment the extracted resume text into structured sections (experience, education, skills, etc.).
    """

    prompt_file = "parser_agent.yaml"

    def run(self, state: ResumeState) -> dict:
        self.logger.info("ParserAgent started")

        if state.get("error"):
            self.logger.warning("Skipping — upstream error detected")
            return {}

        raw_text = state.get("extracted_text", "")
        if not raw_text:
            self.logger.error("No extracted_text found in state")
            return {"error": "No extracted text found in state."}

        # LLM: segment into sections
        try:
            messages = self._build_messages(
                resume_text=raw_text[:6000]
            )  # stay under token limit
            response = self.llm.invoke(messages)
            parsed = self._parse_json_response(response.content)
            self.logger.info(
                f"Parsed sections for: {parsed.get('candidate_name', 'Unknown')}"
            )
            return {
                "parsed_sections": parsed,
            }
        except Exception as exc:
            self.logger.error(f"Section parsing failed: {exc}")
            raise ParserAgentError(f"Section parsing failed: {exc}") from exc
