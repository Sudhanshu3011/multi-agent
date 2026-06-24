from app.agents.base_agent import BaseAgent
from app.core.logger import get_logger
from app.graph.state import ResumeState

logger = get_logger(__name__)


class SkillsAgent(BaseAgent):

    prompt_file = "skills_agent.yaml"

    def __init__(self) -> None:
        super().__init__()
        self._prompt = self._load_prompt()

    def run(self, state: ResumeState) -> dict:
        logger.info("SkillsAgent started")

        if state.get("error"):
            logger.warning("Skipping — upstream error detected")
            return {}

        parsed_sections = state.get("parsed_sections") or {}

        experience = parsed_sections.get("experience", "")
        skills = parsed_sections.get("skills", "")
        projects = parsed_sections.get("projects", "")
        certifications = parsed_sections.get("certifications", "")

        try:
            messages = self._build_messages(
                experience=experience,
                skills=skills,
                projects=projects,
                certifications=certifications,
            )

            response = self.llm.invoke(messages)

            enriched = self._parse_json_response(response.content)

        except Exception as exc:
            logger.warning("LLM enrichment failed, using fallback only", exc_info=True)
            enriched = {}

        skills_analysis = {
            "technical_skills": enriched.get("technical_skills", []),
            "tools_and_platforms": enriched.get("tools_and_platforms", []),
            "domains": enriched.get("domains", []),
        }

        return {"skills_analysis": skills_analysis}
